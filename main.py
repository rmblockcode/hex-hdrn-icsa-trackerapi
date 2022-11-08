import config
import requests

from typing import Union

from fastapi import FastAPI
from fastapi import Path, Query

from utils.base import get_etherscan_request

app = FastAPI()

contracts = {
    'hdrn': {
        'contract_address': '0x3819f64f282bf135d62168c1e513280daf905e06',
        'functions_to_track': [''],
        'decimals': 9
    },
    'icsa': {
        'contract_address': '0xfc4913214444aF5c715cc9F7b52655e788A569ed',
        'functions_to_track': ['icsaStakeStart(uint256 amount)', 'icsaStakeAddCapital(uint256 amount)', 'hdrnStakeStart(uint256 amount)', 'hdrnStakeAddCapital(uint256 amount)'],
        'decimals': 9
    }
}

@app.get("/")
def read_root():
    return {"HEX": "HDRN and ICSA tracker"}

@app.get("/transaction_list/{token_symbol}")
def transaction_list(
    token_symbol: str = Path(
        ...,
        title="Token symbol",
        description="This is token symbol which we will get transactions",
        min_length=1,
        max_length=10,
        )
):
    import time

    params = {
        'module': 'account',
        'action': 'txlist',
        'address': contracts.get(token_symbol).get('contract_address'),
        'sort': 'desc'
    }
    start = time.time()
    success, result = get_etherscan_request(params)

    functions_to_track = contracts.get(
        token_symbol).get('functions_to_track')
    decimals = contracts.get(
        token_symbol).get('decimals')
    result_trx = []

    if success:
        for res in result:
            if  res.get('functionName') in functions_to_track:
                # Getting amount of ERC-20 token transferred
                input = res.get('input')
                amount = int(input.split('00000000')[-1], 16)

                res.update({'amount': amount / (10**decimals)})
                result_trx.append(res)

    response = {'result': result_trx}
    end = time.time()
    print("The time of execution of above program is :",
        (end-start) * 10**3, "ms")
    return response
