import aiohttp
import json
import datetime
import bugsnag

from .fetcher import Fetcher


class LitecoinAPI(Fetcher):

    _URL = 'http://ltc.blockr.io/api/v1/address/balance/{}'

    async def get_ltc_balance(self, loop, address, callback):
        if address is None:
            raise ValueError("address must be specified")
        async with aiohttp.ClientSession(loop=loop) as session:
            endpoint = self._URL.format(address)
            response = await self._fetch(session, endpoint)

            try:
                response = json.loads(response)
                if response.get('status') != 'success':
                    bugsnag.notify(BaseException('LTC request failed'))
                    print(datetime.datetime.now(), 'LTC request failed', response)
                    return
                balance = float(response.get('data').get('balance'))
                multisig_balance = float(response.get('data').get('balance_multisig'))
                amount = balance + multisig_balance
                callback('LTC', amount)
            except:
                bugsnag.notify(BaseException('LTC request failed'))
                print(datetime.datetime.now(), 'LTC request failed', response)
