from fastapi.testclient import TestClient

from main import app

import unittest


class TestHistoryList(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        cls.client.post("/bots/edit",
                    json={
                        "botname": "test",
                        "useful_when": "string",
                        "description": "string",
                        "supported_message_version": [
                            "v1"
                        ],
                        "module_filename": "string",
                        "classname": "string"
                    })

    def test_history_list(self):
        response = self.client.get("/chatlist")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) >= 0)

