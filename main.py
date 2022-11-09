import config
import requests

from typing import Union

from fastapi import FastAPI, Depends
from fastapi import Path, Query

from sqlalchemy.orm import Session
from models import models, schemas, crud

from models.database import SessionLocal, engine

from utils.base import get_etherscan_request

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

contracts = {
    'hdrn': {
        'contract_address': '0x3819f64f282bf135d62168c1e513280daf905e06',
        'functions_to_track': [''],
        'decimals': 9
    },
    'icsa': {
        'contract_address': '0xfc4913214444aF5c715cc9F7b52655e788A569ed',
        'functions_to_track': [
            'icsaStakeStart(uint256 amount)',
            'icsaStakeAddCapital(uint256 amount)',
            'hdrnStakeStart(uint256 amount)',
            'hdrnStakeAddCapital(uint256 amount)'
        ],
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
        ),
    db: Session = Depends(get_db)
):

    # Getting the last queried block
    import pudb; pudb.set_trace()
    last_tx = crud.get_last_contract_transaction(db)
    last_block = last_tx.block_number if last_tx else '0'
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': contracts.get(token_symbol).get('contract_address'),
        'startblock': last_block,
        'sort': 'desc'
    }

    success, result = get_etherscan_request(params)

    functions_to_track = contracts.get(
        token_symbol).get('functions_to_track')
    decimals = contracts.get(
        token_symbol).get('decimals')
    result_trx = []

    if success:
        # If it's not the first execution then remove the first row
        # because it's already stored in database
        if last_block != '0':
            result = result[:-1]
        for res in result:
            if  res.get('functionName') in functions_to_track:
                # Getting amount of ERC-20 token transferred
                input = res.get('input')
                amount = int(input.split('00000000')[-1], 16)

                res.update({'amount': str(amount)})

                # Adding token_symbol to res
                res.update({'token_symbol': token_symbol})

                result_trx.append(res)

    # Saving transactions
    crud.create_contract_transactions(db, result_trx)
    response = {'result': result_trx}

    return response
