import asyncio
import secrets

import httpx
from bs4 import BeautifulSoup

from helper.process_helper import ProcessInit
from helper.parse_hepler import BeautifulSoupAsyncParse
from helper.spider_helper import HttpxAsyncSpider, PyppeteerAsyncSpider


class Mini12(ProcessInit):
    """12MINI快煮鍋"""
    method = "GET"
    url = "https://www.12mini.com.tw/photo_room/str.jpg"
    source_url = "https://www.12mini.com.tw/menu-content.php?menu=2"
    use_spider = HttpxAsyncSpider
    use_parse = BeautifulSoupAsyncParse

    def __init__(self, *args, use_client: httpx.AsyncClient = None, **kwargs):
        super().__init__()

    def get_items(self, parsed: BeautifulSoup = None):
        return [
            self.url
        ]

    async def run(self, *args, **kwargs):
        return {
            self.__class__.__name__: {
                "name": self.__class__.__doc__,
                "data_type": "images",
                "data": self.get_items(),
                "source_url": self.source_url
            },
        }


class McdonaldFullMenu(ProcessInit):
    """麥當勞-全餐"""
    method = "GET"
    url = "https://www.mcdonalds.com/tw/zh-tw/full-menu/extra-value-meals.html"
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


class SuShiTakeOut(ProcessInit):
    """爭鮮GOGO"""
    method = "GET"
    url = "https://www.sushiexpress.com.tw/sushi-take-out/Menu"
    source_url = url
    use_spider = HttpxAsyncSpider
    use_parse = BeautifulSoupAsyncParse

    def __init__(self, *args, use_client: httpx.AsyncClient = None, **kwargs):
        super().__init__()
        self.spider = self.use_spider(use_client=use_client)
        self.spider.update_headers(
            {"Host": "www.sushiexpress.com.tw",
             "cache-control": "no-cache",
             "Cookie": f"ASP.NET_SessionId={secrets.token_hex(12)}",
             }
        )

    def get_items(self, parsed: BeautifulSoup):
        pre_img_path = "https://www.sushiexpress.com.tw"
        donburi = parsed.select("#section_donburi > div > div.grid-item")
        lunchbox = parsed.select("#section_lunchbox > div > div.grid-item")
        return [
            {
                "name": data.find("img").get("alt"),
                "img": f'{pre_img_path}{data.find("img").get("src")}'
            }
            for data in donburi + lunchbox
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


class Omrice888(ProcessInit):
    """洋一咖哩"""
    method = "GET"
    url = "https://www.facebook.com/103527231907858/photos/p.117588047168443/117588047168443"
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


class TonGanCurry(ProcessInit):
    """通庵 熟成咖喱"""
    method = "GET"
    url = "https://live.staticflickr.com/65535/51811665649_72917e8bda_h.jpg"
    source_url = url
    use_spider = HttpxAsyncSpider
    use_parse = BeautifulSoupAsyncParse

    def __init__(self, *args, use_client: httpx.AsyncClient = None, **kwargs):
        super().__init__()

    def get_items(self, parsed: BeautifulSoup = None):
        return [
            self.url
        ]

    async def run(self, *args, **kwargs):
        return {
            self.__class__.__name__: {
                "name": self.__class__.__doc__,
                "data_type": "images",
                "data": self.get_items(),
                "source_url": self.source_url
            },
        }


class SDB1976(ProcessInit):
    """孫東寶"""
    method = "GET"
    url = "http://www.xn--98som070a.tw/menu.html"
    source_url = url
    use_spider = HttpxAsyncSpider
    use_parse = BeautifulSoupAsyncParse

    def __init__(self, *args, use_client: httpx.AsyncClient = None, **kwargs):
        super().__init__()
        self.spider = self.use_spider(use_client=use_client)

    def get_items(self, parsed: BeautifulSoup = None):
        pre_img_path = "http://www.xn--98som070a.tw/"
        foods = parsed.find("div", {"id": "tab4"}).select("div.single-food-inner")
        return [
            {
                "name": data.find("div", {"class": "single-food-item-title"}).find("h2").get_text(),
                "img": f'{pre_img_path}{data.find("img").get("src")}'
            }
            for data in foods
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


async def main():
    async with httpx.AsyncClient(timeout=None) as client:
        print(await SDB1976(use_client=client).run())


if __name__ == '__main__':
    asyncio.run(main())
