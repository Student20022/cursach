from flask import Flask
from flask_restful import Api

from app.site.report.app_routers import router as app_router
from app.api.report.api_routers import router as api_router
from app.api.report.api_routers import (
    DriverResource,
    ReportResource,
    AboutResource,
)


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.register_blueprint(app_router)
    app.register_blueprint(api_router)

    api.add_resource(ReportResource, ReportResource.url)
    api.add_resource(DriverResource, DriverResource.url)
    api.add_resource(AboutResource, AboutResource.url)

    return app
