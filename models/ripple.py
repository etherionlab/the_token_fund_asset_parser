import aiohttp
import json
import datetime
import bugsnag

from .fetcher import Fetcher


class RippleAPI(Fetcher):

    _URL = 'https://data.ripple.com/v2/accounts/{}/balances?currency=XRP'

    async def get_ripple_balance(self, loop, address, callback):
        if address is None:
            raise ValueError("address must be specified")
        async with aiohttp.ClientSession(loop=loop) as session:
            endpoint = self._URL.format(address)
            response = await self._fetch(session, endpoint)

            try:
                response = json.loads(response)
                balance = 0
                for xrp_balance in response.get('balances'):
                    balance += float(xrp_balance.get('value'))
                callback('XRP', balance)
            except:
                bugsnag.notify(BaseException('Ripple request failed'))
                print(datetime.datetime.now(), 'Ripple request failed', response)

