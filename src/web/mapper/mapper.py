from domain.model.field import GameField


def domain_field_to_web_matrix(field: GameField) -> list[list[int]]:
    return [list(row) for row in field.matrix]


def matrix_to_domain_field(matrix: list[list[int]]) -> GameField:
    return GameField(matrix=[list(row) for row in matrix])
