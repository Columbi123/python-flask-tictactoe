import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from main import create_app


class ApiTests(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_create_and_make_move(self):
        response = self.client.post("/game")
        self.assertEqual(response.status_code, 201)
        game = response.get_json()
        self.assertEqual(game["field"], [[0] * 3 for _ in range(3)])
        updated = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
        response = self.client.post(f"/game/{game['uuid']}", json={"field": updated})
        self.assertEqual(response.status_code, 200)
        field = response.get_json()["field"]
        self.assertEqual(sum(x == 1 for row in field for x in row), 1)
        self.assertEqual(sum(x == 2 for row in field for x in row), 1)

    def test_invalid_moves_and_content_type(self):
        game = self.client.post("/game").get_json()
        url = f"/game/{game['uuid']}"
        self.assertEqual(self.client.post(url, data="not json", content_type="text/plain").status_code, 400)
        self.assertEqual(self.client.post(url, json=[]).status_code, 400)
        self.assertEqual(self.client.post(url, json={"field": [[True, 0, 0], [0, 0, 0], [0, 0, 0]]}).status_code, 400)
        self.assertEqual(self.client.post(url, json={"field": [[1, 1, 0], [0, 0, 0], [0, 0, 0]]}).status_code, 400)
        self.assertEqual(self.client.post('/game/not-a-uuid',json={"field": [[0,0,0],[0,0,0],[0,0,0]]}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
