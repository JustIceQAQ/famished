import abc
import asyncio

import httpx
from bs4 import BeautifulSoup

from helper.parse_hepler import AsyncParseInit, BeautifulSoupAsyncParse
from helper.spider_helper import (
    HttpxAsyncSpider,
    AsyncSpiderInit,
    SeleniumAsyncSpider,
    PyppeteerAsyncSpider
)


class ProcessInit(abc.ABC):
    method = None
    url = None
    use_spider: AsyncSpiderInit
    use_parse: AsyncParseInit

    @abc.abstractmethod
    async def get_items(self, parsed: BeautifulSoup):
        raise NotImplementedError

    @abc.abstractmethod
    async def run(self, *args, **kwargs):
        raise NotImplementedError


class DailyBreakfast(ProcessInit):
    """達利早餐"""
    method = "GET"
    url = "https://dailybreakfast.com.tw/dishes/"
    use_spider = HttpxAsyncSpider
    use_parse = BeautifulSoupAsyncParse

    def __init__(self, *args, use_client: httpx.AsyncClient = None, **kwargs):
        super().__init__()
        self.spider = self.use_spider(use_client=use_client)

        self.spider.update_headers({"cookie": "CONSENT=YES+",
                                    "cache-control": "no-cache"})

    def get_items(self, parsed: BeautifulSoup):
        return parsed.select("div.elementor-widget-container > img")

    async def run(self, *args, **kwargs):
        response = await self.spider.fetch(self.method, self.url)
        parsed = await self.use_parse().parsing(response.text)
        return {
            self.__class__.__name__: {
                "name": self.__class__.__doc__,
                "data_type": "images",
                "data": [img["src"] for img in self.get_items(parsed)]
            },
        }


class OnlyToast(ProcessInit):
    """偷吃吐司"""
    method = "GET"
    url = "https://www.facebook.com/111095720641705/photos/p.592458795838726/592458795838726"
    use_spider = PyppeteerAsyncSpider
    use_parse = BeautifulSoupAsyncParse

    def __init__(self, *args, use_client: httpx.AsyncClient = None, **kwargs):
        super().__init__()
        self.spider = self.use_spider()
        self.spider.update_headers({"cache-control": "no-cache"})

    def get_items(self, parsed: BeautifulSoup):
        return parsed.find_all("img", {"data-visualcompletion": "media-vc-image"})

    async def run(self, *args, **kwargs):
        response = await self.spider.fetch(self.method, self.url)
        parsed = await self.use_parse().parsing(response)

        return {
            self.__class__.__name__: {
                "name": self.__class__.__doc__,
                "data_type": "images",
                "data": [img["src"] for img in self.get_items(parsed)]
            },
        }


class YosSoyMilk(ProcessInit):
    """永新豆漿"""
    method = "GET"
    url = "https://www.facebook.com/yossoymilk/photos/p.4983616188376668/4983616188376668"
    use_spider = PyppeteerAsyncSpider
    use_parse = BeautifulSoupAsyncParse

    def __init__(self, *args, use_client: httpx.AsyncClient = None, **kwargs):
        super().__init__()
        self.spider = self.use_spider()
        self.spider.update_headers({"cache-control": "no-cache"})

    def get_items(self, parsed: BeautifulSoup):
        return [parsed.find_all("img", {"data-visualcompletion": "media-vc-image"})[-1]]

    async def run(self, *args, **kwargs):
        response = await self.spider.fetch(self.method, self.url)
        parsed = await self.use_parse().parsing(response)
        return {
            self.__class__.__name__: {
                "name": self.__class__.__doc__,
                "data_type": "images",
                "data": [img["src"] for img in self.get_items(parsed)]
            },
        }


class BrunchFirst(ProcessInit):
    """早餐優選"""
    method = "GET"
    url = "https://www.facebook.com/brunchfirst/photos/p.5280780521973752/5280780521973752"
    use_spider = PyppeteerAsyncSpider
    use_parse = BeautifulSoupAsyncParse

    def __init__(self, *args, use_client: httpx.AsyncClient = None, **kwargs):
        super().__init__()
        self.spider = self.use_spider()
        self.spider.update_headers({"cache-control": "no-cache"})

    def get_items(self, parsed: BeautifulSoup):
        return [parsed.find_all("img", {"data-visualcompletion": "media-vc-image"})[-1]]

    async def run(self, *args, **kwargs):
        response = await self.spider.fetch(self.method, self.url)

        parsed = await self.use_parse().parsing(response)

        data = {
            self.__class__.__name__: {
                "name": self.__class__.__doc__,
                "data_type": "images",
                "data": [img["src"] for img in self.get_items(parsed)]
            },
        }
        return data


class McdonaldBreakfast(ProcessInit):
    """麥當勞-早餐"""
    method = "GET"
    url = "https://www.mcdonalds.com/tw/zh-tw/full-menu/breakfast.html"
    use_spider = HttpxAsyncSpider
    use_parse = BeautifulSoupAsyncParse

    def __init__(self, *args, use_client: httpx.AsyncClient = None, **kwargs):
        super().__init__()
        self.spider = self.use_spider(use_client=use_client)

        self.spider.update_headers({"referer": "https://www.mcdonalds.com/tw/zh-tw.html",
                                    "cache-control": "no-cache"})

    def get_items(self, parsed: BeautifulSoup):
        datas = parsed.select("ul.cmp-category__row > li.cmp-category__item")
        return [
            {
                "name": data.find("div", {"class": "cmp-category__item-name"}).get_text(),
                "img": data.find("img", {"class": "categories-item-img"}).get("src")
            }
            for data in datas
        ]

    async def run(self, *args, **kwargs):
        response = await self.spider.fetch(self.method, self.url)
        parsed = await self.use_parse().parsing(response.text)
        return {
            self.__class__.__name__: {
                "name": self.__class__.__doc__,
                "data_type": "table",
                "columns": ["name", "img"],
                "data": self.get_items(parsed)
            },
        }


if __name__ == '__main__':
    asyncio.run(OnlyToast().run())
