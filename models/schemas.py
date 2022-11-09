from pydantic import BaseModel

class ContractTransactions(BaseModel):
    id: int
    token_symbol: str
    block_number: str
    timestamp: str
    hash: str
    nonce: str
    block_hash: str
    transaction_index: str
    trx_from: str
    trx_to: str
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

    class Config:
        orm_mode = True
