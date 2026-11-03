from dataclasses import dataclass
from uuid import UUID

from datasource.model.field_storage import FieldStorage


@dataclass
class GameStorage:
    uuid: UUID
    field: FieldStorage
