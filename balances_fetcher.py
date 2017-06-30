import asyncio
from datetime import datetime

from models.google_sheets_api import SheetsAPI

from models.etherscan import EtherscanAPI
from models.blockchaininfo import BlockChainInfoAPI
from models.etcchain import EtcChainAPI
from models.waves import WavesAPI
from models.poloniex import PoloniexAPI
from models.kraken import KrakenAPI
from models.litecoin import LitecoinAPI
from models.zcash import ZCashAPI
from models.gamecredits import GameCreditsAPI
from models.dash import DashAPI
from models.ripple import RippleAPI
from models.maidcoin import MaidCoinAPI

from configs import poloniex_keys, kraken_keys

api = SheetsAPI()
ethAPI = EtherscanAPI()
btcAPI = BlockChainInfoAPI()
etcAPI = EtcChainAPI()
wavesAPI = WavesAPI()
gameCreditsAPI = GameCreditsAPI()
litecoinAPI = LitecoinAPI()
zcashAPI = ZCashAPI()
rippleAPI = RippleAPI()
dashAPI = DashAPI()
maidAPI = MaidCoinAPI()
poloniexAPI = PoloniexAPI(poloniex_keys.KEY, poloniex_keys.SECRET)
krakenAPI = KrakenAPI(kraken_keys.KEY, kraken_keys.SECRET)

addresses = {}
balances = {}

poloniex_assets = set()
kraken_assets = set()


def replace(symbol):
    if symbol == 'ICONOMI':
        return 'ICN'
    if symbol == 'GOLEM':
        return 'GNT'
    return symbol


def on_amount_received(symbol, amount):
    global balances
    balances[replace(symbol)] = balances.get(replace(symbol), 0) + amount


def on_poloniex_balances_received(poloniex_balances):
    global balances, poloniex_assets
    for asset in poloniex_assets:
        _balance = poloniex_balances.get(asset, {'available': '0.00000000', 'btcValue': '0.00000000', 'onOrders': '0.00000000'})
        balance = float(_balance['onOrders']) + float(_balance['available'])
        balances[replace(asset)] = balances.get(replace(asset), 0) + balance


def on_kraken_balances_received(kraken_balances):
    global balances, kraken_assets
    for asset in kraken_assets:
        prefix = 'Z' if asset == 'EUR' or asset == 'USD' else 'X'
        if asset == 'BTC': asset = 'XBT'
        balance = float(kraken_balances.get(prefix + asset, '0.0'))
        if asset == 'XBT': asset = 'BTC'
        balances[replace(asset)] = balances.get(replace(asset), 0) + balance


def fetch_balances():
    global balances, addresses, poloniex_assets, kraken_assets

    balances = {}
    # read addresses from the spreadsheet
    addresses = api.read_addresses()

    loop = asyncio.get_event_loop()

    asset_futures = []
    for (symbol, place, address) in addresses:
        if place == 'Static':
            balances[replace(symbol)] = balances.get(replace(symbol), 0) + float(address)
            continue
        if place == "Poloniex":
            poloniex_assets.add(symbol)
            continue
        if place == "Kraken":
            kraken_assets.add(symbol)
            continue
        if symbol == "ETH":
            future = ethAPI.get_ether_balance(
                loop,
                address=address,
                callback=on_amount_received
            )
        elif symbol == "BTC":
            future = btcAPI.get_btc_balance(
                loop,
                address=address,
                callback=on_amount_received
            )
        elif symbol == "ICN":
            future = ethAPI.get_tokens_balance(
                loop,
                address=address,
                token='ICONOMI',
                decimals=18,
                callback=on_amount_received
            )
        elif symbol == "HMQ":
            future = ethAPI.get_tokens_balance_by_address(
                loop,
                address=address,
                token='HMQ',
                contract_address='0xcbcc0f036ed4788f63fc0fee32873d6a7487b908',
                decimals=8,
                callback=on_amount_received
            )
        elif symbol == 'LH':
            future = ethAPI.get_tokens_balance_by_address(
                loop,
                address=address,
                token='LH',
                contract_address='0x6531f133e6DeeBe7F2dcE5A0441aA7ef330B4e53',
                decimals=8,
                callback=on_amount_received
            )
        elif symbol == 'GNT':
            future = ethAPI.get_tokens_balance_by_address(
                loop,
                address=address,
                token='GNT',
                contract_address='0xa74476443119A942dE498590Fe1f2454d7D4aC0d',
                decimals=18,
                callback=on_amount_received
            )
        elif symbol == 'REP':
            future = ethAPI.get_tokens_balance_by_address(
                loop,
                address=address,
                token='REP',
                contract_address='0x48c80F1f4D53D5951e5D5438B54Cba84f29F32a5',
                decimals=18,
                callback=on_amount_received
            )
        elif symbol == "MLN":
            future = ethAPI.get_tokens_balance_by_address(
                loop,
                address=address,
                token='MLN',
                contract_address='0xBEB9eF514a379B997e0798FDcC901Ee474B6D9A1',
                decimals=18,
                callback=on_amount_received
            )
        elif symbol == "ANT":
            future = ethAPI.get_tokens_balance_by_address(
                loop,
                address=address,
                token='ANT',
                contract_address='0x960b236A07cf122663c4303350609A66A7B288C0',
                decimals=18,
                callback=on_amount_received
            )
        elif symbol == "BCAP":
            future = ethAPI.get_tokens_balance_by_address(
                loop,
                address=address,
                token='BCAP',
                contract_address='0xff3519eeeea3e76f1f699ccce5e23ee0bdda41ac',
                decimals=0,
                callback=on_amount_received
            )
        elif symbol == 'BAT':
            future = ethAPI.get_tokens_balance_by_address(
                loop,
                address=address,
                token='BAT',
                contract_address='0x0D8775F648430679A709E98d2b0Cb6250d2887EF',
                decimals=18,
                callback=on_amount_received
            )
        elif symbol == 'SNT':
            future = ethAPI.get_tokens_balance_by_address(
                loop,
                address=address,
                token='SNT',
                contract_address='0x744d70FDBE2Ba4CF95131626614a1763DF805B9E',
                decimals=18,
                callback=on_amount_received
            )
        elif symbol == "ETC":
            future = etcAPI.get_etc_balance(
                loop,
                address=address,
                callback=on_amount_received
            )
        elif symbol == "WAVES":
            future = wavesAPI.get_waves_balance(
                loop,
                address=address,
                callback=on_amount_received
            )
        elif symbol == "GAME":
            future = gameCreditsAPI.get_gamecredits_balance(
                loop,
                address=address,
                callback=on_amount_received
            )
        elif symbol == "LTC":
            future = litecoinAPI.get_ltc_balance(
                loop,
                address=address,
                callback=on_amount_received
            )
        elif symbol == "ZEC":
            future = zcashAPI.get_zcash_balance(
                loop,
                address=address,
                callback=on_amount_received
            )
        elif symbol == "XRP":
            future = rippleAPI.get_ripple_balance(
                loop,
                address=address,
                callback=on_amount_received
            )
        elif symbol == "DASH":
            future = dashAPI.get_dash_balance(
                loop,
                address=address,
                callback=on_amount_received
            )
        elif symbol == "MAID":
            future = maidAPI.get_maid_balance(
                loop,
                address=address,
                callback=on_amount_received
            )
        else:
            print("unknown symbol:", symbol)
            continue
        asset_futures.append(future)

    asset_futures.append(poloniexAPI.get_balances(loop, callback=on_poloniex_balances_received))
    asset_futures.append(krakenAPI.get_balances(loop, callback=on_kraken_balances_received))
    loop.run_until_complete(asyncio.gather(*asset_futures))
    #
    # here all async requests already finished
    #

    asset_names, asset_symbols = api.read_balances_assets()

    # compose new line
    date = datetime.now().strftime('%Y-%m-%d %H:%M')
    row = [date]

    for symbol in asset_symbols:
        row.append(balances.get(symbol, ''))

    api.add_balances_row(row)
    return balances

if __name__ == '__main__':
    fetch_balances()
