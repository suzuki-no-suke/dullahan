from fastapi.testclient import TestClient

from main import app

import unittest


class TestHistoryList(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_history_list(self):
        response = self.client.get("/chatlist")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) >= 0)

