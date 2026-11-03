class DomainError(Exception):
    """Базовое исключение для ошибок предметной области."""

    pass


class InvalidMoveError(DomainError):
    pass


class GameOverError(DomainError):
    pass


class GameNotFoundError(DomainError):
    pass
