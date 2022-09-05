import abc

from bs4 import BeautifulSoup

from helper.parse_hepler import AsyncParseInit
from helper.spider_helper import AsyncSpiderInit


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
