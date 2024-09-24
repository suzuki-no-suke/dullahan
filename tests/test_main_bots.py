from fastapi.testclient import TestClient

from main import app

import unittest

class TestBotsInfo(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        cls.client.post("/bots/edit",
                    json={
                        "botname": "echobot",
                        "display_name": "echobot",
                        "useful_when": "string",
                        "description": "string",
                        "supported_message_version": [
                            "v1"
                        ],
                        "module_filename": "v1.Echobot",
                        "classname": "Echobot"
                    })

    def test_bots_list(self):
        response = self.client.get("/bots/list")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        names = [d["botname"] for d in data]
        self.assertIn("test", names)

    def test_bots_detail(self):
        response = self.client.get("/bots/detail/test")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual("test", data['botname'])

    def test_bots_edit_detail(self):
        response = self.client.get("/bots/edit/test")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual("test", data['botname'])
        self.assertIn("module_filename", data.keys())
        self.assertIn("classname", data.keys())

    def test_bots_edit_detail_post(self):
        # data update
        data = {
            "botname": "echobot",
            "display_name": "test",
            "useful_when": "testing",
            "description": "unfound",
            "supported_message_version": [
                "v1"
            ],
            "module_filename": "string",
            "classname": "string"
        }

        response = self.client.post("/bots/edit",
                                    json=data)
        self.assertEqual(response.status_code, 200)
        retdata = response.json()
        self.assertEqual(200, retdata['status'])


