from fastapi.testclient import TestClient

from main import app

import unittest

from src.datadef.enums.chat_status import ChatStatus


class TestChatSequence(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        cls.client.post("/bots/edit",
                    json={
                        "botname": "test",
                        "display_name": "test",
                        "useful_when": "string",
                        "description": "string",
                        "supported_message_version": [
                            "v1"
                        ],
                        "module_filename": "v1.Echobot",
                        "classname": "Echobot"
                    })

    def test_create_and_get_chat(self):
        # create
        response = self.client.get("/v1/chat/history/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["history_id"])
        self.assertEqual("waiting", data["chat_status"])
        self.assertEqual("v1", data["message_version"])

        history_id = data["history_id"]

        # get
        response = self.client.get(f"/v1/chat/history/{history_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["history_id"])
        self.assertEqual("waiting", data["chat_status"])
        self.assertEqual("v1", data["message_version"])

    def test_chatting(self):
        # create
        response = self.client.get("/v1/chat/history/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["history_id"])
        self.assertEqual("waiting", data["chat_status"])
        self.assertEqual("v1", data["message_version"])

        history_id = data["history_id"]

        # send message
        chatdata = {
            "sender_type": "human",
            "botname": "test",
            "agent": "human",
            "content": "hello world",
        }
        response = self.client.post(f"/v1/chat/send?history_id={history_id}", json=chatdata)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(history_id, data['history_id'])
        self.assertGreaterEqual(2, len(data['messages']))
        self.assertIsNotNone(data['messages'][0]['message_id'])
        self.assertIsNotNone(data['messages'][1]['message_id'])


    def test_continue_chatting(self):
        # list
        response = self.client.get("/chatlist")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        history_id = data[0]["history_id"]

        # add new chat
        chatdata = {
            "sender_type": "human",
            "botname": "test",
            "agent": "human",
            "content": "hello world",
        }
        response = self.client.post(f"/v1/chat/send?history_id={history_id}", json=chatdata)
        self.assertEqual(response.status_code, 200)

        # access history
        response = self.client.get(f"/v1/chat/history/{history_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(history_id, data["history_id"])
        self.assertGreaterEqual(len(data["messages"]), 2)


