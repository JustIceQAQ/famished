import asyncio
import os
from typing import Union, Dict, Any

import httpx
import requests
import abc
from pyppeteer import launch

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from requests import Response


class SpiderInit(abc.ABC):
    @abc.abstractmethod
    def fetch(self, *args, **kwargs):
        raise NotImplementedError


class AsyncSpiderInit(abc.ABC):
    headers = {
        "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/104.0.0.0 Safari/537.36")
    }

    def update_headers(self, _dict):
        self.headers.update(_dict)

    @abc.abstractmethod
    async def fetch(self, *args, **kwargs):
        raise NotImplementedError


class RequestsSpider(SpiderInit):
    def __init__(self, method: str, url: str, **kwargs: Dict[str, Any]):
        self.request = requests.request
        self.method = method
        self.url = url
        self.requests_kwargs = kwargs

    def fetch(self, *args, **kwargs) -> Union[Response, Response]:
        return self.request(self.method, self.url, **self.requests_kwargs)


class HttpxAsyncSpider(AsyncSpiderInit):
    def __init__(self, use_client: httpx.AsyncClient = None):
        super().__init__()
        self.use_client = httpx.AsyncClient if use_client is None else use_client

    async def fetch(self, method: str, url: str, *args, **kwargs) -> Union[Response, Response]:
        return await self.use_client.request(method, url, headers=self.headers, **kwargs)


class SeleniumAsyncSpider(AsyncSpiderInit):
    def __init__(self, ):
        super().__init__()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-notifications")
        self.use_client = webdriver.Chrome(executable_path=ChromeDriverManager(cache_valid_range=7).install(),
                                           options=options)

    async def fetch(self, method: str, url: str, *args, **kwargs) -> str:
        self.use_client.get(url)
        page_source = self.use_client.page_source
        self.use_client.quit()
        return page_source


class PyppeteerAsyncSpider(AsyncSpiderInit):
    def __init__(self, ):
        pass

    async def fetch(self, method: str, url: str, *args, **kwargs) -> str:
        deploy_level = os.getenv("deploy_level", "dev")
        if deploy_level in {"prod"}:
            browser = await launch(
                executablePath='/usr/bin/google-chrome-stable',
                headless=True,
                options={'args': ["--no-sandbox", "--disable-notifications"]},
            )
        else:
            browser = await launch(
                headless=True,
                options={'args': ["--no-sandbox", "--disable-notifications"]},
            )
        page = await browser.newPage()
        await page.goto(url, waitUntil="networkidle0")
        page_source = await page.content()
        await browser.disconnect()
        await browser.close()
        return page_source
