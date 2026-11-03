from uuid import UUID

from datasource.mapper.game_mapper import GameMapper
from datasource.repository.interface import GameRepository
from datasource.repository.storage import InMemoryStorage

from domain.exceptions import GameNotFoundError
from domain.model.game import Game


class InMemoryGameRepository(GameRepository):
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def save(self, game: Game) -> None:

        storage_game = GameMapper.to_storage(game)

        self.storage.save(storage_game)

    def get(self, uuid: UUID) -> Game:

        storage_game = self.storage.get(uuid)

        if storage_game is None:
            raise GameNotFoundError(f"Game {uuid} not found")
        return GameMapper.to_domain(storage_game)

    def exists(self, uuid: UUID) -> bool:
        return self.storage.exists(uuid)
