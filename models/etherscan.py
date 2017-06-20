import aiohttp
import json
import datetime
import bugsnag

from .fetcher import Fetcher


class EtherscanAPI(Fetcher):

    _URL = 'https://api.etherscan.io/api?'

    async def get_ether_balance(self, loop, address, callback):
        if address is None:
            raise ValueError("address must be specified")
        async with aiohttp.ClientSession(loop=loop) as session:
            endpoint = self._URL + "module=account&action=balance&address={}".format(address)
            response = await self._fetch(session, endpoint)

            try:
                response = json.loads(response).get('result')
                amount = float(response) / 10 ** 18  # from wei to ETH
                callback('ETH', amount)
            except:
                bugsnag.notify(BaseException('ETH request failed'))
                print(datetime.datetime.now(), 'ETH request failed', response)

    async def get_tokens_balance(self, loop, address, token, decimals, callback):
        if address is None:
            raise ValueError("address must be specified")
        async with aiohttp.ClientSession(loop=loop) as session:
            endpoint = self._URL + "module=account&action=tokenbalance&address={}&tokenname={}".format(address, token)
            response = await self._fetch(session, endpoint)

            try:
                response = json.loads(response)
                message = response.get('message')
                if message == 'NOTOK':
                    raise ValueError("{} doesn't exist".format(token))
                amount = float(response.get('result')) / (10 ** decimals)
                callback(token, amount)
            except:
                bugsnag.notify(BaseException('Token balance request failed'))
                print(datetime.datetime.now(), 'Token balance request failed', response)

    async def get_tokens_balance_by_address(self, loop, address, token, contract_address, decimals, callback):
        if address is None:
            raise ValueError("address must be specified")
        async with aiohttp.ClientSession(loop=loop) as session:
            endpoint = self._URL + "module=account&action=tokenbalance&contractaddress={}&address={}".format(contract_address, address)
            response = await self._fetch(session, endpoint)

            try:
                response = json.loads(response)
                message = response.get('message')
                if message == 'NOTOK':
                    bugsnag.notify(BaseException('Token doesnt\' exist'.format(token)))
                    print(datetime.datetime.now(), "{} doesn't exist".format(token))
                    return
                amount = float(response.get('result')) / (10 ** decimals)
                callback(token, amount)
            except:
                bugsnag.notify(BaseException('Token balance request failed'))
                print(datetime.datetime.now(), 'Token balance request failed', response)

    async def get_total_supply(self, loop, contract_address, callback):
        async with aiohttp.ClientSession(loop=loop) as session:
            endpoint = self._URL + "module=account&action=tokensupply&contractaddress={}".format(contract_address)
            response = await self._fetch(session, endpoint)

            try:
                response = json.loads(response)
                message = response.get('message')
                if message == 'NOTOK':
                    bugsnag.notify(BaseException('Can\'t read total supply from contract {}'.format(contract_address)))
                    print(datetime.datetime.now(), "Can't read total supply from contract {}".format(contract_address))
                    return
                amount = float(response.get('result'))
                callback(amount)
            except:
                bugsnag.notify(BaseException('TotalTokenSupply request failed'))
                print(datetime.datetime.now(), 'TotalTokenSupply request failed', response)
