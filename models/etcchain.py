import aiohttp
import json
import datetime
import bugsnag

from .fetcher import Fetcher


class EtcChainAPI(Fetcher):

    _URL = 'https://etcchain.com/api/v1/getAddressBalance?address={}'

    async def get_etc_balance(self, loop, address, callback):
        if address is None:
            raise ValueError("address must be specified")
        async with aiohttp.ClientSession(loop=loop) as session:
            endpoint = self._URL.format(address)
            response = await self._fetch(session, endpoint)

            try:
                response = json.loads(response)
                balance = float(response.get('balance'))
                callback('ETC', balance)
            except:
                bugsnag.notify(BaseException('ETC request failed'))
                print(datetime.datetime.now(), 'ETC request failed', response)
