from uuid import uuid4

from domain.exceptions import InvalidMoveError, GameOverError

from domain.model.field import GameField
from domain.model.game import Game
from domain.service.interface import GameService

from datasource.repository.interface import GameRepository

from dataclasses import replace


class GameServiceImpl(GameService):
    def __init__(self, repository: GameRepository):
        self.repository = repository

    def validate_field(self, game: Game, updated_field: GameField) -> None:
        saved_game = self.repository.get(game.uuid)
        if game.field != saved_game.field:
            raise InvalidMoveError("Provided game state does not match stored state")
        finished, _ = self.is_game_over(game)
        if finished:
            raise GameOverError("Game is already over")

        old = game.field.matrix
        new = updated_field.matrix
        changes = 0
        for r in range(3):
            for c in range(3):
                if old[r][c] != new[r][c]:
                    if old[r][c] != 0 or new[r][c] != 1:
                        raise InvalidMoveError(f"Invalid change at ({r},{c})")
                    changes += 1
        if changes != 1:
            raise InvalidMoveError("Exactly one move required")

    def is_game_over(self, game: Game) -> tuple[bool, int | None]:

        field = game.field.matrix

        lines = []

        lines.extend(field)

        for col in range(3):
            lines.append([field[0][col], field[1][col], field[2][col]])

        lines.append([field[0][0], field[1][1], field[2][2]])

        lines.append([field[0][2], field[1][1], field[2][0]])

        for line in lines:
            if line[0] != 0 and len(set(line)) == 1:
                return True, line[0]

        if game.field.is_full():
            return True, None

        return False, None

    def get_next_move(self, game: Game) -> tuple[int, int]:
        finished, _ = self.is_game_over(game)
        if finished:
            raise GameOverError("Game is already over")

        empty = game.field.get_empty_cells()
        if not empty:
            raise GameOverError("No empty cells")

        best_score = -float("inf")
        best_move = empty[0]
        for row, col in empty:
            new_matrix = [list(r) for r in game.field.matrix]
            new_matrix[row][col] = 2
            new_field = GameField(matrix=tuple(tuple(r) for r in new_matrix))
            score = self._minimax(new_field, depth=0, is_maximizing=False)
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_move

    def _minimax(self, field: GameField, depth: int, is_maximizing: bool) -> int:
        temp_game = Game(uuid=uuid4(), field=field)
        finished, winner = self.is_game_over(temp_game)
        if finished:
            if winner == 2:
                return 10 - depth
            elif winner == 1:
                return -10 + depth
            else:
                return 0

        empty = field.get_empty_cells()
        if not empty:
            return 0

        if is_maximizing:
            best = -float("inf")
            for row, col in empty:
                new_matrix = [list(row) for row in field.matrix]
                new_matrix[row][col] = 2
                new_field = GameField(matrix=new_matrix)
                score = self._minimax(new_field, depth + 1, False)
                best = max(best, score)
            return best
        else:
            best = float("inf")
            for row, col in empty:
                new_matrix = [list(row) for row in field.matrix]
                new_matrix[row][col] = 1
                new_field = GameField(matrix=new_matrix)
                score = self._minimax(new_field, depth + 1, True)
                best = min(best, score)
            return best

    def apply_computer_move(self, game: Game) -> Game:
        finished, _ = self.is_game_over(game)
        if finished:
            return game

        row, col = self.get_next_move(game)

        new_matrix = [list(r) for r in game.field.matrix]
        new_matrix[row][col] = 2
        new_field = GameField(matrix=new_matrix)

        return replace(game, field=new_field)
