import aiohttp
import xml.etree.ElementTree as ET
from .fetcher import Fetcher
import datetime
import bugsnag


class EuropeanCBAPI(Fetcher):

    _URL = 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'

    async def get_eur_usd_exchange_rate(self, loop, callback):
        async with aiohttp.ClientSession(loop=loop) as session:
            response = await self._fetch(session, self._URL)

            try:
                tree = ET.fromstring(response)
                for rate in tree[2][0]:
                    if rate.get('currency') == 'USD':
                        callback(rate.get('rate'))
                        break
            except:
                bugsnag.notify(BaseException('European CB request failed'))
                print(datetime.datetime.now(), 'European CB request failed', response)
