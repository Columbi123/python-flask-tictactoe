from abc import ABC, abstractmethod

from domain.model.game import Game
from domain.model.field import GameField


class GameService(ABC):
    @abstractmethod
    def get_next_move(self, game: Game) -> tuple[int, int]:
        pass

    @abstractmethod
    def validate_field(self, game: Game, updated_field: GameField) -> None:
        pass

    @abstractmethod
    def is_game_over(self, game: Game) -> tuple[bool, int | None]:
        pass

    @abstractmethod
    def apply_computer_move(self, game: Game) -> Game:
        pass
