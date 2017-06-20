import aiohttp
import json
import datetime
import bugsnag

from .fetcher import Fetcher


class GameCreditsAPI(Fetcher):

    _URL = 'http://159.203.226.245:3000/api/addr/{}/?noTxList=1'

    async def get_gamecredits_balance(self, loop, address, callback):
        if address is None:
            raise ValueError("address must be specified")
        async with aiohttp.ClientSession(loop=loop) as session:
            endpoint = self._URL.format(address)
            response = await self._fetch(session, endpoint)

            try:
                response = json.loads(response).get('balance')
                amount = float(response)
                callback('GAME', amount)
            except:
                bugsnag.notify(BaseException('GAME request failed'))
                print(datetime.datetime.now(), 'GAME request failed', response)
