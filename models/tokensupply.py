import aiohttp
import json
import datetime
import bugsnag

from .fetcher import Fetcher


class TokenSupplyAPI(Fetcher):

    _URL = 'https://tkn.jwma.ru/api/stats'

    async def get_token_supply(self, loop, callback):
        async with aiohttp.ClientSession(loop=loop) as session:
            response = await self._fetch(session, self._URL)

            try:
                response = json.loads(response).get('count')
                amount = float(response)
                callback(amount)
            except:
                bugsnag.notify(BaseException('TotalSupply request failed'))
                print(datetime.datetime.now(), 'TotalSupply request failed', response)

