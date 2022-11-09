from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from . import models, schemas

def create_contract_transactions(db: Session, list_transactions: list):
    for transaction in list_transactions[::-1]:
        try:
            data = {
                "token_symbol": transaction.get("token_symbol"),
                "block_number": transaction.get("blockNumber"),
                "tx_timestamp": transaction.get("timeStamp"),
                "hash": transaction.get("hash"),
                "nonce": transaction.get("nonce"),
                "block_hash": transaction.get("blockHash"),
                "transaction_index": transaction.get("transactionIndex"),
                "tx_from": transaction.get("from"),
                "tx_to": transaction.get("to"),
                "value": transaction.get("value"),
                "gas": transaction.get("gas"),
                "gas_price": transaction.get("gasPrice"),
                "is_error": transaction.get("isError"),
                "txreceipt_status": transaction.get("txreceipt_status"),
                "input": transaction.get("input"),
                "contract_address": transaction.get("contractAddress"),
                "cumulative_gas_used": transaction.get("cumulativeGasUsed"),
                "gas_used": transaction.get("gasUsed"),
                "confirmations": transaction.get("confirmations"),
                "method_id": transaction.get("methodId"),
                "function_name": transaction.get("functionName"),
                "amount": transaction.get("amount"),
            }

            new_contract_tx = models.ContractTransactions(**data)
            db.add(new_contract_tx)
            db.commit()
            db.refresh(new_contract_tx)
        except SQLAlchemyError as e:
            print('ERROR saving the following transaction: ' + str(data))
            print(str(e))
            continue
    return

def get_last_contract_transaction(db: Session):
    return db.query(models.ContractTransactions).order_by(
        models.ContractTransactions.id.desc()).first()        