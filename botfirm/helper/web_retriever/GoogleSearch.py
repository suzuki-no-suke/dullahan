from googleapiclient.discovery import build

import traceback

class GoogleSearch:
    def __init__(self, api_key, cse_id):
        self.api_key = api_key
        self.cse_id = cse_id

    def search(self, query):
        result = {
            "succeed": False,
            "query": query,
            "message": "",
            "results": []
        }
        try:
            service = build("customsearch", "v1", developerKey=self.api_key)
            res = (
                service.cse()
                    .list(
                        q=query,
                        cx=f"{self.cse_id}"
                    )
                    .execute()
            )
            result["results"] = res
        except Exception as ex:
            result["message"] = f"web search failed : query {query} / ex {ex}"
        return result
