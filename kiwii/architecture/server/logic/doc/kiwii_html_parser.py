import sysconfig
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Tuple, Optional

from kiwii.architecture.server.logic.doc.consts import KIWII_URL, PYTHON_STDLIB_URL
from kiwii.architecture.shared.routes import DOC_ROUTE
from kiwii.shared.path_utils import normalize, urijoin


class KiwiiHTMLParser(HTMLParser):
    """
    Custom `html.parser.HTMLParser` with additional encoding functionality hacked in.

    The problem:
    `pydoc` renders HTML for local viewing only, meaning all the `href` values lead to `pydoc` rendered
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
    """

    def __init__(self, module: str):
        super().__init__(convert_charrefs=False)

        self.module_path: Path = Path(module.replace('.', '/'))
        self.encoded: str = ""

    def local_to_external_file_url(self, path: str) -> str:
        """
        `pydoc` adds local 'file:' style links to rendered HTML leading to the file/module. This method ensures that:
        - local links lead to external python doc links
        - links that lead to modules (that end with `__init__.py`) lead to appropriate `__init__.py` files
        - links that lead to files (that end with `.py`) lead to appropriate `.py` files

        Returns external URL which matches the provided local file URL.
        """

        # decode URI encoding
        unquoted_path = urllib.parse.unquote(path)

        # strip "file:" protocol and convert to actual Path
        if unquoted_path.startswith("file:"):
            real_path = Path(unquoted_path[5:])
        else:
            real_path = Path(unquoted_path)

        # resolve docs url based on if the module is standard library or kiwii
        # one advantage of being a standard library only module is that I don't have to consider any other module >:D
        #
        # now, Windows paths suck - multiple slashes can be present and directory names are not case-sensitive
        # therefore we must completely normalize both paths in order to use `startswith` here
        if normalize(str(real_path)).startswith(normalize(sysconfig.get_path('stdlib'))):
            code_url = PYTHON_STDLIB_URL
        else:
            code_url = KIWII_URL

        # resolve final part of the filename
        if real_path.name == '__init__.py':
            file_uri = self.module_path / real_path.name
        else:
            file_uri = self.module_path.parent / f"{self.module_path.name}.py"

        return urijoin(code_url.geturl(), file_uri.as_posix())

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        """
        Encodes all start tags as-is, unless they are `<a>` tags, in which case:
        - all relative documentation links are prepended with the kiwii doc URI
        - all local `file:` references are re-encoded to lead to actual external code
        """

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
                        v = urijoin(DOC_ROUTE.path, v)

                fixed_attrs.append((k, v))

        # encode back to HTML
        self.encoded += f"<{tag} {' '.join([f'{k}={chr(34)}{v}{chr(34)}' for k, v in fixed_attrs])}".strip() + ">"

    def handle_endtag(self, tag: str) -> None:
        """Encodes all end tags as-is."""

        self.encoded += f"</{tag}>"

    def handle_data(self, data: str) -> None:
        """
        Encodes all plaintext data tags as-is, unless they are local file paths, in which case they are rewritten
        to lead to external code.
        """

        # assume data is path
        path: Path = Path(data)

        # if path is absolute (filters out all plaintext HTML data) and is an actual file - replace with external URL
        if path.is_absolute() and path.is_file():
            data = self.local_to_external_file_url(data)

        self.encoded += data

    def handle_decl(self, decl: str) -> None:
        """Encodes all doctype declarations as-is."""

        self.encoded += f"<!{decl}>"

    def handle_entityref(self, name: str) -> None:
        """Encodes all entity references as-is."""

        self.encoded += f"&{name}"
