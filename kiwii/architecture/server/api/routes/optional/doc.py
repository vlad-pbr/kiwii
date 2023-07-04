from email.message import Message
from http import HTTPStatus

from kiwii import __name__ as top_module_name
from kiwii.architecture.server.api import register
from kiwii.architecture.server.api.shared.models import RouteParams
from kiwii.architecture.server.logic.doc.doc import render_module_doc_html
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.routes import DOC_ROUTE, DocRouteParams
from kiwii.shared.path_utils import urijoin


@register(DOC_ROUTE)
def doc(params: RouteParams[DocRouteParams]) -> Response:
    """
    Documentation route handler:
    - redirects to top level module documentation if module path parameter was not specified
    - returns re-encoded HTML back to client
    """

    # if no module is specified - redirect to top module (kiwii) documentation
    if params.path_params.module is None:
        headers = Message()
        headers.add_header("Location", urijoin(DOC_ROUTE.path, f"{top_module_name}.html"))

        return Response(status=HTTPStatus.PERMANENT_REDIRECT, headers=headers)

    # render module documentation
    module_doc_html = render_module_doc_html(params.path_params.module)
    if not module_doc_html:
        return Response(status=HTTPStatus.NOT_FOUND)

    return Response(status=HTTPStatus.OK, body=module_doc_html)
