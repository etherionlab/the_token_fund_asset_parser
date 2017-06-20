import aiohttp
import datetime
from .fetcher import Fetcher
import bugsnag


class MaidCoinAPI(Fetcher):

    _URL = 'http://omniexplorer.info/ask.aspx?api=getbalance&prop=3&address={}'

    async def get_maid_balance(self, loop, address, callback):
        if address is None:
            raise ValueError("address must be specified")
        async with aiohttp.ClientSession(loop=loop) as session:
            endpoint = self._URL.format(address)
            response = await self._fetch(session, endpoint)

            try:
                balance = float(response)
                callback('MAID', balance)
            except:
                bugsnag.notify(BaseException('MAID request failed'))
                print(datetime.datetime.now(), 'MAID request failed', response)
