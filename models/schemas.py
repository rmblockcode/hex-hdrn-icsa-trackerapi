from typing import List
from enum import Enum
from pydantic import BaseModel

from datetime import datetime


class FunctionsName(Enum):
    icsa_stake_start = 'icsaStakeStart'
    icsa_stake_add_capital = 'icsaStakeAddCapital'
    hdrn_stake_start = 'hdrnStakeStart'
    hdrn_stake_add_capital = 'hdrnStakeAddCapital'


class ContractTransactions(BaseModel):
    id: int
    create_date: datetime
    token_symbol: str
    block_number: str
    tx_timestamp: str
    hash: str
    nonce: str
    block_hash: str
    transaction_index: str
    tx_from: str
    tx_to: str
    value: str
    gas: str
    gas_price: str
    is_error: str
    txreceipt_status: str
    input: str
    contract_address: str
    cumulative_gas_used: str
    gas_used: str
    confirmations: str
    method_id: str
    function_name: str
    amount: str
    approximate_amount_usd: float
    token_price: float

    class Config:
        orm_mode = True


class StatsByFunctionName(BaseModel):
    icsa_stake_start: List[ContractTransactions]

    pass
