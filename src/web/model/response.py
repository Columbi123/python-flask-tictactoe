from uuid import UUID
from typing import List


class GameResponse:
    def __init__(self, uuid: UUID, field: List[List[int]]):
        self.uuid = uuid
        self.field = field

    def to_json(self) -> dict:
        return {"uuid": str(self.uuid), "field": self.field}
