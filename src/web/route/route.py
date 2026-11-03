from flask import jsonify
from web.module.handlers import create_game_handler, update_game_handler


def register_routes(app, repository, service):
    """
    Регистрирует все маршруты приложения.
    """

    @app.route("/game", methods=["POST"])
    def create_game():
        data, status = create_game_handler(repository)
        return jsonify(data), status

    @app.route("/game/<uuid_str>", methods=["POST"])
    def handle_update_game(uuid_str):
        data, status = update_game_handler(uuid_str, repository, service)
        return jsonify(data), status
