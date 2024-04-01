from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    Response,
)

from tabulate import tabulate
from typing import Any

from app.utils.web.utils import get_results, desc_result
from app.utils.web.serializers import (
    serialize_report,
    serialize_drivers,
)


router = Blueprint('app_routers', __name__)


@router.route('/')
def index():
    return redirect('/report')


@router.route('/report')
@router.route('/report/')
def report_page() -> Response:
    request_order = request.args.get('order', 'asc')

    result = get_results()
    if request_order == 'desc':
        result = desc_result(result)

    serialized_data = [info.dict() for info in serialize_report(result)]

    return Response(
        tabulate(serialized_data, headers='keys', tablefmt='jira'),
        content_type='text/plain; charset=utf-8',
    )


@router.route('/report/drivers/')
def driver_list() -> str:
    request_order = request.args.get('order', 'asc')
    result = get_results()

    if request_order == 'desc':
        result = desc_result(result)

    return render_template('drivers.html', info=serialize_drivers(result))


@router.route('/report/drivers')
def about_driver() -> list[dict[str, Any]]:
    abbr = request.args.get('abbr')

    serialized_data = [
        info.dict() for info in serialize_report(get_results(abbr=abbr))
    ]

    return serialized_data
