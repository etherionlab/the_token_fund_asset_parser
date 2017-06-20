import aiohttp
import json
import datetime
import bugsnag

from .fetcher import Fetcher


class DashAPI(Fetcher):

    _URL = 'https://api.blockcypher.com/v1/dash/main/addrs/{}'

    async def get_dash_balance(self, loop, address, callback):
        if address is None:
            raise ValueError("address must be specified")
        async with aiohttp.ClientSession(loop=loop) as session:
            endpoint = self._URL.format(address)
            response = await self._fetch(session, endpoint)

            try:
                response = json.loads(response)
                balance = response.get("final_balance") / 10 ** 8
                callback('DASH', balance)
            except:
                bugsnag.notify(BaseException('DASH request failed'))
                print(datetime.datetime.now(), 'DASH request failed', response)
