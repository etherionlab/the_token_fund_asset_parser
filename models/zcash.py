import aiohttp
import json
import datetime
import bugsnag

from .fetcher import Fetcher


class ZCashAPI(Fetcher):

    _URL = 'https://api.zcha.in/v2/mainnet/accounts/{}'

    async def get_zcash_balance(self, loop, address, callback):
        if address is None:
            raise ValueError("address must be specified")
        async with aiohttp.ClientSession(loop=loop) as session:
            endpoint = self._URL.format(address)
            response = await self._fetch(session, endpoint)

            try:
                response = json.loads(response)
                balance = float(response.get("balance"))
                callback('ZEC', balance)
            except:
                bugsnag.notify(BaseException('ZCash request failed'))
                print(datetime.datetime.now(), 'ZCash request failed', response)
