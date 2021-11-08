from helpers.base_api_client import BaseApiClient
from settings import API_KEY


class CovalentApi(BaseApiClient):
    HOST = "https://api.covalenthq.com"
    BASE_API_URL = "{}/v1/"
    KEY = API_KEY
    CHAIN_IDS = {
        "Ethereum": 1,
        "Polygon / Matic": 137,
        "Avalanche C - Chain": 43114,
        "Binance Smart Chain": 56,
        "Fantom Opera": 250,
        "RSK": 30,
        "Arbitrum": 42161,
        "Palm": 11297108109,
        "Klaytn": 8217,
        "HECO": 128,
        "Moonriver": 1285
    }
    TOKENS = {}

    def __init__(self):
        self.host = self.HOST
        self.base_url = self.BASE_API_URL.format(self.host)
        self.key = self.KEY
        self.tokens_data = self.get_token_data()
        self.token_list = self.get_token_list()

    def get_token_list(self):
        return [x['contract_ticker_symbol'] for x in self.tokens_data['data']['items']]

    def get_dex_health(self, chain_id: int = 1, dexname: str = "sushiswap"):
        """Get the health status of the Uniswap clone DEX. Returns the latest sync block.
        :param chain_id: Covalent ID of blockchain
        :param dexname: Market maker name
        :return: json data
        """
        url = "{}{}/xy=k/{}/{}".format(self.base_url, chain_id, dexname, "health")
        request = self.get(url)
        return request.json()

    def get_dex_ecosystem(self, chain_id: int = 1, dexname: str = "sushiswap"):
        """
        Get Uniswap clone ecosystem data. Returns total volume and total liquidity chart data over the last 30 days.
        :param chain_id: Covalent ID of blockchain
        :param dexname: Market maker name
        :return: json data
        """
        url = "{}{}/xy=k/{}/{}".format(self.base_url, chain_id, dexname, "ecosystem")
        request = self.get(url)
        return request.json()

    def get_dex_pool(self, chain_id: int = 1, dexname: str = "sushiswap"):
        """
        Get Uniswap clone pool data.
        :param chain_id: Covalent ID of blockchain
        :param dexname: Market maker name
        :return: json data
        """

        url = "{}{}/xy=k/{}/{}".format(self.base_url, chain_id, dexname, "pools")
        request = self.get(url)
        data = request.json()
        data_items_list = data["data"]["items"]

        while data["data"]["pagination"]["has_more"]:
            print(data["data"]["pagination"])
            page = data["data"]["pagination"]["page_number"]
            request = self.get(url, page_number=page+1)
            data_ = request.json()
            data_items_list.extend(data_["data"]["items"])
            data = request.json()
        return {"data": {"items": data_items_list, "pagination": data["data"]["pagination"]}}

    def get_pool_by_address(self, address: str, chain_id: int = 1, dexname: str = "sushiswap"):
        """
        Get Uniswap clone pool data by address. Includes 7 day and 30 day volume and liquidity chart data.
        :param address:
        :param chain_id:
        :param dexname:
        :return:
        """
        url = "{}{}/xy=k/{}/pools/address/{}".format(self.base_url, chain_id, dexname, address)
        request = self.get(url)
        return request.json()

    def get_txn_by_address(self, address: str, chain_id: int =1, dexname: str = "sushiswap"):
        """
        Get Uniswap clone pool transactions by address. Returns the latest 20 swap, mint and burn events.
        :param address:
        :param chain_id:
        :param dexname:
        :return:
        """
        url = "{}{}/xy=k/{}/pools/address/{}/transactions".format(self.base_url, chain_id, dexname, address)
        request = self.get(url)
        return request.json()

    def get_token_data(self, chain_id: int = 1, dexname: str = "sushiswap"):
        """
        Get Uniswap clone token data.
        :param address:
        :param chain_id:
        :param dexname:
        :return:
        """
        url = "{}{}/xy=k/{}/tokens".format(self.base_url, chain_id, dexname)
        request = self.get(url)
        return request.json()

    def get_tokens_by_address(self, address: str, chain_id: int = 1, dexname: str = "sushiswap"):
        """
        Get Uniswap clone pool data by address. Includes 7 day and 30 day volume, liquidity and pricing chart data.
        :param address:
        :param chain_id:
        :param dexname:
        :return:
        """
        url = "{}{}/xy=k/{}/tokens/address/{}".format(self.base_url, chain_id, dexname, address)
        request = self.get(url)
        return request.json()

    def get_token_txns_by_address(self, address: str, chain_id: int = 1, dexname: str = "sushiswap"):
        """
        Get Uniswap clone pool token transactions by address. Returns the latest 20 swap, mint and burn events.
        Example using WETH contract address
        :param address: '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
        :param chain_id:
        :param dexname:
        :return:
        """
        url = "{}{}/xy=k/{}/tokens/address/{}/transactions".format(self.base_url, chain_id, dexname, address)
        request = self.get(url)
        return request.json()

    def get_lp_balance_by_address(self, address: str, chain_id: int = 1, dexname: str = "sushiswap"):
        """
        Get Uniswap clone address exchange balances. Returns the LP balances of the address.
        :param address:
        :param chain_id:
        :param dexname:
        :return:
        """
        url = "{}{}/xy=k/{}/address/{}/balances".format(self.base_url, chain_id, dexname, address)
        request = self.get(url)
        return request.json()

    def get_exchange_liquidity_txns_by_address(self, address: str, chain_id: int = 1, dexname: str = "sushiswap"):
        """
        Get Uniswap clone address exchange liquidity transactions.
        :param address: '0x1f14be60172b40dac0ad9cd72f6f0f2c245992e8'
        :param chain_id:
        :param dexname:
        :return:
        """
        url = "{}{}/xy=k/{}/address/{}/transactions".format(self.base_url, chain_id, dexname, address)
        request = self.get(url)
        return request.json()


if __name__ == "__main__":
    weth_addrs = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    api = CovalentApi()
    sushi_health_data = api.get_dex_health()
    sushi_ecosystem_data = api.get_dex_ecosystem()
    sushi_pool_data = api.get_dex_pool()

    pools_from_address = api.get_pool_by_address(address="0xceff51756c56ceffca006cd410b03ffc46dd3a58")
    txns_from_address = api.get_txn_by_address(address="0xceff51756c56ceffca006cd410b03ffc46dd3a58")

    token_data = api.get_token_data()
    tokens_from_address = api.get_tokens_by_address(address="0xceff51756c56ceffca006cd410b03ffc46dd3a58") # not sure what address type to use
    token_txns_from_address = api.get_token_txns_by_address(address="0xceff51756c56ceffca006cd410b03ffc46dd3a58") # same

    lp_balance_data = api.get_lp_balance_by_address(address="0xceff51756c56ceffca006cd410b03ffc46dd3a58")
    liquidity_txn_data = api.get_exchange_liquidity_txns_by_address(address="0xceff51756c56ceffca006cd410b03ffc46dd3a58") #same