from typing import Optional

from datasource.repository.storage import InMemoryStorage
from datasource.repository.repository import InMemoryGameRepository
from datasource.repository.interface import GameRepository

from domain.service.interface import GameService
from domain.service.impl import GameServiceImpl


class Container:
    def __init__(self):
        self._storage: Optional[InMemoryStorage] = None
        self._repository: Optional[GameRepository] = None
        self._service: Optional[GameService] = None

    def get_storage(self) -> InMemoryStorage:

        if self._storage is None:
            self._storage = InMemoryStorage()

        return self._storage

    def get_repository(self) -> GameRepository:

        if self._repository is None:
            self._repository = InMemoryGameRepository(self.get_storage())

        return self._repository

    def get_service(self) -> GameService:

        if self._service is None:
            self._service = GameServiceImpl(self.get_repository())

        return self._service
