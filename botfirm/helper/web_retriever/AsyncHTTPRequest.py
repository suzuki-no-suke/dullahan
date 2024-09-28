import aiohttp
from dataclasses import dataclass

import aiohttp.client_exceptions
import aiohttp.http_exceptions
from bs4 import BeautifulSoup

@dataclass
class RetrievedData:
    title: str
    full_html: str
    description: str
    text_body: str

    def __str__(self) -> str:
        description = self.description[:50] if self.description else '---'
        text_body = self.text_body[:100] if self.text_body else '---'
        return f"WebRetrieved -> {self.title}, {description} : {text_body}"

import enum

class RequestStatus(enum.Enum):
    NotFinished = "not_finished"
    InvalidURL = "invalid_url"
    NotFound = "not_found"
    Found = "found"

@dataclass
class GetResult:
    status: RequestStatus
    message: str
    htmldata: str

    def __str__(self) -> str:
        return f"GetResult -> {self.status}, {self.message} : {self.htmldata[:50] if self.htmldata else '---'}"


class AsyncHTTPRequest:
    def __init__(self, url):
        self.url = url
        self.full_html = None

    async def get(self):
        response = GetResult(status=RequestStatus.NotFinished, message="", htmldata="")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    if response.status == 200:
                        self.full_html = await response.text()

                        response.status = RequestStatus.Found
                        response.method = "success"
                        response.htmldata = self.full_html
        except aiohttp.client_exceptions.InvalidUrlClientError:
            response.status = RequestStatus.InvalidURL
            response.message = "invalid url"
        except aiohttp.client_exceptions.ClientConnectionError:
            response.status = RequestStatus.NotFound
            response.message = "not found"
        return response

    def analysis(self, parser="html5lib"):
        """parse loaded webpage (html) and
        title, description (meta), html text (all text).

        if data notfound, it set to empty ("")
        """
        if self.full_html is None:
            raise ValueError("you need to get first")

        # parse with bs4
        soup = BeautifulSoup(self.full_html, parser)

        # retrieve information
        data = RetrievedData(full_html=self.full_html, title="", description="", text_body="")

        # タイトルの取得
        title_tag = soup.find('title')
        data.title = title_tag.string if title_tag else ""

        # メタ説明の取得
        meta_description = soup.find('meta', attrs={'name': 'description'})
        data.description = meta_description['content'] if meta_description else ""

        # ボディのテキストのみを取得
        data.text_body = soup.get_text(strip=True)

        return data


    def analysis_with_python_default(self):
        return self.analysis(parser="html.parser")
