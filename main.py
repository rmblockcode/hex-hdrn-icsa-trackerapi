import config
import requests

from typing import Union, Optional
from fastapi import FastAPI, Depends
from fastapi import Path, Query

# Schedule iport s
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from datetime import date
from fastapi_scheduler import SchedulerAdmin
#

from sqlalchemy.orm import Session
from models import models, schemas, crud

from models.database import SessionLocal, engine

from utils import base
from utils.notifications import discord_notifications

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Create `AdminSite` instance
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"HEX": "HDRN and ICSA tracker"}

@app.get(
    "/transaction_list/{token_symbol}",
    response_model=list[schemas.ContractTransactions]
)
def transaction_list(
    token_symbol: str = Path(
        ...,
        title="Token symbol",
        description="This is token symbol which we will get transactions",
        min_length=1,
        max_length=10,
        ),
    start_block: Optional[str] = Query(
        None,
        title="Start block",
        description="Start block to perform the search. Use this field only the first execution",
        min_length=1,
        max_length=20
        ),
    db: Session = Depends(get_db)
):

    if not start_block:
        # Getting the last queried block
        last_tx = crud.get_last_contract_transaction(db)
        start_block = last_tx.block_number if last_tx else '0'

    params = {
        'module': 'account',
        'action': 'txlist',
        'address': config.contracts.get(token_symbol).get('contract_address'),
        'startblock': start_block,
        'sort': 'desc'
    }

    success, result = base.get_etherscan_request(params)

    functions_to_track = config.contracts.get(
        token_symbol).get('functions_to_track')
    decimals = config.contracts.get(token_symbol).get('decimals') * -1
    result_trx = []

    if success:
        for res in result:
            if  res.get('functionName') in functions_to_track:
                # Getting amount of ERC-20 token transferred
                input = res.get('input')
                amount = base.get_etc20_transferred(input, decimals)

                res.update({'amount': str(amount)})

                # Adding token_symbol to res
                res.update({'token_symbol': token_symbol})

                result_trx.append(res)

    # Saving transactions
    new_transactions = crud.create_contract_transactions(db, result_trx)

    # Creating notifications
    discord_notifications(db, new_transactions)
    return new_transactions


@app.get("/stats_by_functions_name")
def stats_by_functions_name(
    function_name: Optional[schemas.FunctionsName] = Query(
        None,
        title="Function name",
        description="Name of the function to be queried",
        example="icsaStakeStart"
        ),
    db: Session = Depends(get_db)
):
    return crud.get_transactions_by_function_name(db, function_name)


############################################

# Create an instance of the scheduled task scheduler `SchedulerAdmin`
scheduler = SchedulerAdmin.bind(site)

# Add scheduled tasks, refer to the official documentation: https://apscheduler.readthedocs.io/en/master/
# use when you want to run the job at fixed intervals of time
#@scheduler.scheduled_job('interval', seconds=60)
def interval_task():
    print('Executing transaction list...')
    base.run_local_request()
    print('Process Finished')


@app.on_event("startup")
async def startup():
    # Mount the background management system
    site.mount_app(app)
    # Start the scheduled task scheduler
    scheduler.start()