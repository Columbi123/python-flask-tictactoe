from dataclasses import dataclass
from uuid import UUID, uuid4

from domain.model.field import GameField


@dataclass
class Game:
    uuid: UUID
    field: GameField

    @classmethod
    def create_new(cls):

        return cls(
            uuid=uuid4(), field=GameField(matrix=[[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        )
