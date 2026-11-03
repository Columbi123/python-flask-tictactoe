import os

from flask import Flask

from di.container import Container

from web.route.route import register_routes


def create_app():

    app = Flask(__name__)

    container = Container()

    register_routes(app, container.get_repository(), container.get_service())

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
