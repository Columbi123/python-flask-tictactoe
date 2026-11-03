from typing import List


class UpdateGameRequest:
    def __init__(self, field: List[List[int]]):
        self.field = field

    @classmethod
    def from_json(cls, data: dict) -> "UpdateGameRequest":
        if not isinstance(data, dict):
            raise ValueError("JSON body must be an object")
        field = data.get("field")
        if field is None:
            raise ValueError("Missing 'field' in request body")
        if not isinstance(field, list) or len(field) != 3:
            raise ValueError("Field must be a 3x3 matrix")
        for row in field:
            if not isinstance(row, list) or len(row) != 3:
                raise ValueError("Field must be a 3x3 matrix")
            for cell in row:
                if type(cell) is not int or cell not in (0, 1, 2):
                    raise ValueError("Cell values must be 0, 1, or 2")
        return cls(field)
