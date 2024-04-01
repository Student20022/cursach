from typing import Any
import simplexml

from flask_restful import Resource
from flask import Response, request, jsonify, Blueprint

from app.utils.web.utils import get_results
from app.utils.web.serializers import serialize_report, serialize_drivers


router = Blueprint('api_routers', __name__)


def format_arg(data: list[dict[str, Any]]) -> Response:
    if request.args.get('format') == 'xml':
        return Response(
            simplexml.dumps({'report': data}),
            content_type='application/xml',
        )
    return jsonify(data)


class ReportResource(Resource):
    url = '/api/v1/report/'

    def get(self) -> Response:
        serialized_data = [
            info.dict() for info in serialize_report(get_results())
        ]

        return format_arg(serialized_data)


class DriverResource(Resource):
    url = '/api/v1/report/drivers/'

    def get(self) -> Response:
        serialized_data = [
            info.dict() for info in serialize_drivers(get_results())
        ]

        return format_arg(serialized_data)


class AboutResource(Resource):
    url = '/api/v1/report/drivers/about/'

    def get(self) -> Response:
        abbr = request.args.get('abbr')

        serialized_data = [
            info.dict() for info in serialize_report(get_results(abbr=abbr))
        ]

        return format_arg(serialized_data)
