import aiohttp
import json

from .fetcher import Fetcher


class Asset:

    def __init__(self, name, symbol, price_usd, price_btc, date):
        self.name = name
        self.symbol = symbol
        self.price_USD = float(price_usd)
        self.price_BTC = float(price_btc)
        self.date = date

    def __str__(self, *args, **kwargs):
        return 'Asset("name": {}, "symbol": {}, "usd price": {}, "btc price": {}, "date": {})'.format(
            self.name, self.symbol, self.price_USD, self.price_BTC, self.date
        )

    def __repr__(self):
        return self.__str__()


class CoinmarketcapAPI(Fetcher):
    _COINMARKETCAP_URL = 'https://api.coinmarketcap.com/v1/ticker?limit={}'

    def __init__(self, assets_limit=150):
        self._ASSETS_LIMIT = assets_limit

    async def request_assets(self, loop, assets, callback=None):
        async with aiohttp.ClientSession(loop=loop) as session:
            ticker = await self._fetch(session, self._COINMARKETCAP_URL.format(self._ASSETS_LIMIT))
            ticker = json.loads(ticker)
            prices = [Asset(asset.get("name"),
                            asset.get("symbol"),
                            asset.get("price_usd"),
                            asset.get("price_btc"),
                            int(asset.get("last_updated", -1)) or -1)
                      for asset in ticker if asset.get("symbol") in assets]
            if callback is not None:
                callback(prices)
        return prices
