import pydoc
import sysconfig
import platform
from http import HTTPMethod, HTTPStatus
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional, Tuple, List

from kiwii import __name__ as top_module_name, __pythondocs__ as kiwii_docs_url
from kiwii.architecture.server.api import register
from kiwii.architecture.server.api.shared.models import RouteParams
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.route_paths import DOC_ROUTE_PATTERN, DOC_ROUTE_PATH

PYTHON_STDLIB_URL: str = f"https://github.com/python/cpython/tree/{'.'.join(platform.python_version_tuple()[:2])}/Lib"


class KiwiiHTMLParser(HTMLParser):
    """
    Custom `html.parser.HTMLParser` with additional encoding functionality hacked in.

    The problem:
    `pydoc` renders HTML for local viewing only, meaning all of the `href` values lead to `pydoc` rendered
    HTML files and even local `.py` files for the modules themselves via `file:` protocol. This, of course, does not
    work when exposing documentation over remote API - HTML files do not reside on the server and `.py` files are
    not located on the client's machine.

    The solution:
    Middleware between the `pydoc`'s rendered HTML and the actual response body for the client which edits the `href`
    values to lead clients back to the API. However, `html.parser.HTMLParser` only handles the parsing of HTML and
    does provide any API for editing it (which, unironically, makes complete sense - it's called a parser for a reason).
    This is where the hack comes in. `html.parser.HTMLParser` provides handlers for when it encounters start (<...>) and
    end (</...>) HTML tags as it parses the HTML. These handlers are called chronologically as the parser encounters
    these tags. Kiwii leverages these handler calls by recombining the HTML back to the original value, editing the
    `href` values along the way and storing the re-encoded HTML in a custom class property. This property can then
    be safely returned to the client. Yeah.

    TODO this class does not belong here, move it to the appropriate directory
    """

    def __init__(self, module: str):
        super().__init__(convert_charrefs=False)

        self.module_path: str = f"{module.replace('.', '/')}"
        self.encoded: str = ""

    def local_to_external_file_url(self, path: str) -> str:
        """
        `pydoc` adds local 'file:' style links to rendered HTML leading to the file/module. This method ensures that:
        - local links lead to external python doc link
        - links that lead to modules (that end with `__init__.py`) lead to appropriate `__init__.py` files
        - links that lead to files (that end with `.py`) lead to appropriate `.py` files

        Returns external URL which matches the provided local file URL.
        """

        # strip "file:" protocol
        if path.startswith("file:"):
            path_no_protocol = Path(path[5:])
        else:
            path_no_protocol = Path(path)

        # resolve docs url based on if the module is standard library or kiwii
        # one advantage of being a standard library only module is that I don't have to consider any other module >:D
        if str(path_no_protocol).startswith(sysconfig.get_path('stdlib')):
            docs_url = PYTHON_STDLIB_URL
        else:
            docs_url = kiwii_docs_url

        # resolve final part of the filename
        if str(path_no_protocol).endswith('__init__.py'):
            filename: str = f'/{path_no_protocol.name}'
        else:
            filename: str = '.py'

        return f"{docs_url}/{self.module_path}{filename}"

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:

        # TODO inject <style>

        # re-encode `href` values
        fixed_attrs: List[Tuple[str, Optional[str]]] = []
        if tag != "a":
            fixed_attrs = attrs
        else:
            for k, v in attrs:
                if k == "href":

                    # keep external links intact
                    if v.startswith("http"):
                        pass

                    # keep relative anchor links intact
                    elif v.startswith("#"):
                        pass

                    # redirect all `file:` references to external module code
                    elif v.startswith("file:"):
                        v = self.local_to_external_file_url(v)

                    # prepend all href values with documentation URI
                    else:
                        v = f"{DOC_ROUTE_PATH}/{v}"

                fixed_attrs.append((k, v))

        # encode back to HTML
        self.encoded += f"<{tag} {' '.join([f'{k}={chr(34)}{v}{chr(34)}' for k, v in fixed_attrs])}".strip() + ">"

    def handle_endtag(self, tag: str) -> None:
        self.encoded += f"</{tag}>"

    def handle_data(self, data: str) -> None:

        # assume data is path
        path: Path = Path(data)

        # if path is absolute (filters out all plaintext HTML data) and is an actual file - replace with external URL
        if path.is_absolute() and path.is_file():
            data = self.local_to_external_file_url(data)

        self.encoded += data

    def handle_decl(self, decl: str) -> None:
        self.encoded += f"<!{decl}>"

    def handle_entityref(self, name: str) -> None:
        self.encoded += f"&{name}"


def writedoc(thing: str) -> str:
    """
    Repurposed version of pydoc `writedoc` method which returns the generated HTML page
    instead of writing to file.

    Yes, `thing` is the original parameter name and I ain't changing it.
    """

    _object, _name = pydoc.resolve(thing, False)
    return pydoc.html.page(pydoc.describe(_object), pydoc.html.document(_object, _name))


@register(HTTPMethod.GET, DOC_ROUTE_PATTERN)
def doc(params: RouteParams) -> Response:
    """
    Documentation route handler:
    - reads the requested module path parameter
    - renders HTML for the requested module using `pydoc`'s underlying methods
    - re-encodes `pydoc`'s HTML output using custom `html.parser.HTMLParser`
    - returns re-encoded HTML back to client
    """

    # resolve module that is being documented
    module = params.path_params[0] if params.path_params[0] else top_module_name

    # encode HTML data returned by pydoc using custom HTML parser
    parser = KiwiiHTMLParser(module=module)
    try:
        parser.feed(writedoc(module))
    except ImportError:
        return Response(status=HTTPStatus.NOT_FOUND)

    return Response(status=HTTPStatus.OK, body=parser.encoded)
