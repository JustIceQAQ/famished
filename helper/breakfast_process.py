import asyncio

import httpx
from bs4 import BeautifulSoup

from helper.parse_hepler import BeautifulSoupAsyncParse
from helper.process_helper import ProcessInit
from helper.spider_helper import (
    HttpxAsyncSpider,
    PyppeteerAsyncSpider
)


class DailyBreakfast(ProcessInit):
    """達利早餐"""
    method = "GET"
    url = "https://dailybreakfast.com.tw/dishes/"
    source_url = url
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
                "data": [img["src"] for img in self.get_items(parsed)],
                "source_url": self.source_url
            },
        }


class OnlyToast(ProcessInit):
    """偷吃吐司"""
    method = "GET"
    url = "https://www.facebook.com/111095720641705/photos/p.592458795838726/592458795838726"
    source_url = url
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
                "data": [img["src"] for img in self.get_items(parsed)],
                "source_url": self.source_url
            },
        }


class YosSoyMilk(ProcessInit):
    """永新豆漿"""
    method = "GET"
    url = "https://www.facebook.com/yossoymilk/photos/p.4983616188376668/4983616188376668"
    source_url = url
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
                "data": [img["src"] for img in self.get_items(parsed)],
                "source_url": self.source_url
            },
        }


class BrunchFirst(ProcessInit):
    """早餐優選"""
    method = "GET"
    url = "https://www.facebook.com/brunchfirst/photos/p.5280780521973752/5280780521973752"
    source_url = url
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
                "data": [img["src"] for img in self.get_items(parsed)],
                "source_url": self.source_url
            },
        }
        return data


class McdonaldBreakfast(ProcessInit):
    """麥當勞-早餐"""
    method = "GET"
    url = "https://www.mcdonalds.com/tw/zh-tw/full-menu/breakfast.html"
    source_url = url
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
                "data": self.get_items(parsed),
                "source_url": self.source_url
            },
        }


if __name__ == '__main__':
    asyncio.run(OnlyToast().run())
