from datasource.model.field_storage import FieldStorage
from datasource.model.game_storage import GameStorage

from domain.model.field import GameField
from domain.model.game import Game


class GameMapper:
    @staticmethod
    def to_storage(game: Game) -> GameStorage:
        return GameStorage(uuid=game.uuid, field=FieldStorage(matrix=game.field.matrix))

    @staticmethod
    def to_domain(storage: GameStorage) -> Game:
        return Game(uuid=storage.uuid, field=GameField(matrix=storage.field.matrix))
