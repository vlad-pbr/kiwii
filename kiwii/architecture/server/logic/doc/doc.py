import pydoc
from typing import Optional

from kiwii.architecture.server.logic.doc.kiwii_html_parser import KiwiiHTMLParser


def writedoc(thing: str) -> str:
    """
    Repurposed version of pydoc `writedoc` method which returns the generated HTML page
    instead of writing to file.

    Yes, `thing` is the original parameter name and I ain't changing it.
    """

    _object, _name = pydoc.resolve(thing, False)
    return pydoc.html.page(pydoc.describe(_object), pydoc.html.document(_object, _name))


def render_module_doc_html(module: str) -> Optional[str]:
    """
    Module documentation HTML generator:
    - renders HTML for the requested module using `pydoc`'s underlying methods
    - re-encodes `pydoc`'s HTML output using custom `html.parser.HTMLParser`

    Returns module documentation HTML as string.
    Return None if module was not found.
    """

    # encode HTML data returned by pydoc using custom HTML parser
    parser = KiwiiHTMLParser(module=module)
    try:
        parser.feed(writedoc(module))
        return parser.encoded
    except ImportError:
        return None
