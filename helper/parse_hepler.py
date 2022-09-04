import abc

from bs4 import BeautifulSoup


class AsyncParseInit(abc.ABC):
    @abc.abstractmethod
    async def parsing(self, *args, **kwargs):
        raise NotImplementedError


class BeautifulSoupAsyncParse(AsyncParseInit):
    async def parsing(self, context, features="html5lib"):
        return BeautifulSoup(context, features)
