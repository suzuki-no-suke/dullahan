import asyncio

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from botfirm.helper.web_retriever.AsyncHTTPRequest import AsyncHTTPRequest

if __name__=="__main__":
    # URL invalid
    target = AsyncHTTPRequest("!u")
    call_result = asyncio.run(target.get())
    print(f"get result -> expect invalid url : actual {call_result}")

    # found
    target = AsyncHTTPRequest("http://google.co.jp/")
    call_result = asyncio.run(target.get())
    print(f"get result -> expect found : actual {call_result.htmldata[:50]}")
    analysis_result = target.analysis()
    print(analysis_result)

    # not found
    target = AsyncHTTPRequest("http://everyday-not-found.com/")
    call_result = asyncio.run(target.get())
    print(f"get result -> expect invalid url : actual {call_result}")
