import os

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
ETHERSCAN_API_URL = os.getenv('ETHERSCAN_API_URL')
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL').replace("postgres://", "postgresql://", 1)
COINGECKO_API = os.getenv('COINGECKO_API')
API_URL = os.getenv('API_URL')

contracts = {
    'hdrn': {
        'contract_address': '0x3819f64f282bf135d62168c1e513280daf905e06',
        'functions_to_track': [
            'loanLiquidateBid(uint256 liquidationId, uint256 liquidationBid)'],
        'decimals': 9,
        'min_amount_in_usd_to_track': 1000
    },
    'icsa': {
        'contract_address': '0xfc4913214444aF5c715cc9F7b52655e788A569ed',
        'functions_to_track': [
            'icsaStakeStart(uint256 amount)',
            'icsaStakeAddCapital(uint256 amount)',
            'hdrnStakeStart(uint256 amount)',
            'hdrnStakeAddCapital(uint256 amount)'
        ],
        'decimals': 9,
        'min_amount_in_usd_to_track': None
    }
}