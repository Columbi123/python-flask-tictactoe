from threading import Lock
from uuid import UUID
from typing import Dict, Optional
from datasource.model.game_storage import GameStorage


class InMemoryStorage:
    def __init__(self):
        self._games: Dict[UUID, GameStorage] = {}
        self._lock = Lock()

    def save(self, game: GameStorage) -> None:
        with self._lock:
            self._games[game.uuid] = game

    def get(self, uuid: UUID) -> Optional[GameStorage]:
        with self._lock:
            return self._games.get(uuid)

    def exists(self, uuid: UUID) -> bool:
        with self._lock:
            return uuid in self._games
