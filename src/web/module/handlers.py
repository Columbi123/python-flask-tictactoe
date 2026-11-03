from dataclasses import replace
from uuid import UUID
from flask import request
from domain.exceptions import InvalidMoveError, GameOverError, GameNotFoundError
from domain.model.game import Game
from domain.service.interface import GameService
from datasource.repository.interface import GameRepository
from web.model.request import UpdateGameRequest
from web.model.response import GameResponse
from web.model.error_response import ErrorResponse
from web.mapper.mapper import (
    matrix_to_domain_field,
    domain_field_to_web_matrix,
)


def create_game_handler(repository: GameRepository):
    game = Game.create_new()
    repository.save(game)
    return {
        "uuid": str(game.uuid),
        "field": game.field.matrix,
    }, 201


def update_game_handler(
    uuid_str: str, repository: GameRepository, service: GameService
):
    try:
        game_uuid = UUID(uuid_str)
    except ValueError:
        return ErrorResponse("Invalid UUID format").to_json(), 400

    json_data = request.get_json(silent=True)
    if json_data is None:
        return ErrorResponse("Invalid JSON body").to_json(), 400
    try:
        req = UpdateGameRequest.from_json(json_data)
    except ValueError as e:
        return ErrorResponse("Invalid request data", str(e)).to_json(), 400

    try:
        current_game = repository.get(game_uuid)
    except GameNotFoundError:
        return ErrorResponse("Game not found").to_json(), 404

    try:
        updated_field = matrix_to_domain_field(req.field)
    except ValueError as e:
        return ErrorResponse("Invalid field data", str(e)).to_json(), 400

    try:
        service.validate_field(current_game, updated_field)
    except (InvalidMoveError, GameOverError) as e:
        return ErrorResponse("Validation failed", str(e)).to_json(), 400

    updated_game = replace(current_game, field=updated_field)

    updated_game = service.apply_computer_move(updated_game)

    repository.save(updated_game)

    response = GameResponse(
        uuid=updated_game.uuid, field=domain_field_to_web_matrix(updated_game.field)
    )
    return response.to_json(), 200
