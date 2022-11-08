import requests
import config

def get_etherscan_request(params):
    try:
        params.update({
            'apikey': config.API_KEY,
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