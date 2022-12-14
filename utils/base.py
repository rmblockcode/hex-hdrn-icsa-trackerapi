import requests
import config

def run_local_request(token_symbol):
    requests.get(config.API_URL + 'transaction_list/' + token_symbol)

def get_etherscan_request(params):
    try:
        params.update({
            'apikey': config.ETHERSCAN_API_KEY,
        })

        response = requests.get(
            config.ETHERSCAN_API_URL, params=params
        )
        
        response = response.json()
    
        # Successfully
        if response.get('status') == '1':
            return True, response.get('result')
        
        return False, {'message': response.get('result')}
    except Exception as e:
        print(str(e))
        return False, {}

def get_token_prices_in_usd():
    endpoint_url = config.COINGECKO_API + \
        'simple/price?ids=hedron,icosa&vs_currencies=usd'

    try:
        response = requests.get(endpoint_url)
        return response.json()
    except Exception as e:
        print('Error getting prices from coingecko: ' + str(e))
        raise e


def get_etc20_transferred(data, decimals):
    amount = str(int(data.split('00000000')[-1], 16))
    return f'{amount[:decimals]}.{amount[decimals:]}'