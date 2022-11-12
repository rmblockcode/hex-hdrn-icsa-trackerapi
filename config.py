import os

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
ETHERSCAN_API_URL = os.getenv('ETHERSCAN_API_URL')
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL').replace("postgres://", "postgresql://", 1)
COINGECKO_API = os.getenv('COINGECKO_API')
API_URL = os.getenv('API_URL')