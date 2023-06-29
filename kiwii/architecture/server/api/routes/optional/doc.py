import pydoc
from http import HTTPMethod, HTTPStatus
from html.parser import HTMLParser
from typing import Optional, Tuple, List

from kiwii import __name__ as top_module_name
from kiwii.architecture.server.api import register
from kiwii.architecture.server.api.shared.models import RouteParams
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.route_paths import DOC_ROUTE_PATTERN, DOC_ROUTE_PATH


class KiwiiHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.encoded: str = ""

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:

        # TODO inject <style>
        # TODO anchor links
        # TODO external links

        # prepend all href values with documentation URI
        # redirect all `file:/` references to self
        fixed_attrs: List[Tuple[str, Optional[str]]] = []
        for k, v in attrs:
            if tag == "a" and k == "href":
                if v.startswith("file:/"):
                    v = ""
                else:
                    v = f"{DOC_ROUTE_PATH}/{v}"
            fixed_attrs.append((k, v))

        # encode back to HTML
        self.encoded += f"<{tag} {' '.join([f'{k}={chr(34)}{v}{chr(34)}' for k, v in fixed_attrs])}".strip() + ">"

    def handle_endtag(self, tag: str) -> None:
        self.encoded += f"</{tag}>"

    def handle_data(self, data: str) -> None:
        self.encoded += data

    def handle_decl(self, decl: str) -> None:
        self.encoded += f"<!{decl}>"


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

    # encode HTML data returned by pydoc using custom HTML parser
    parser = KiwiiHTMLParser()
    try:
        parser.feed(writedoc(params.path_params[0] if params.path_params[0] else top_module_name))
    except ImportError:
        return Response(status=HTTPStatus.NOT_FOUND)

    return Response(status=HTTPStatus.OK, body=parser.encoded)
