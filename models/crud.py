import config

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from . import models, schemas
from utils.base import get_token_prices_in_usd


def create_contract_transactions(db: Session, list_transactions: list):
    result_list = []

    # Getting token prices
    token_prices = get_token_prices_in_usd()

    for transaction in list_transactions[::-1]:
        try:

            # First check if the transaction is not already added into the database
            exists = db.query(models.ContractTransactions).filter(
                models.ContractTransactions.block_hash==transaction.get("blockHash")
            ).first()

            if exists:
                continue

            amount = float(transaction.get('amount'))
            if transaction.get('functionName').startswith('icsa'):
                price = token_prices.get('icosa').get('usd')
            else:
                price = token_prices.get('hedron').get('usd')

            approximate_amount_usd = amount * price

            min_amount = config.contracts.get(
                transaction.get('token_symbol')).get('min_amount_in_usd_to_track')

            # Only store transactions with amounts in usd >= than configure in the contracto            
            if min_amount and approximate_amount_usd >= min_amount:
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
                    "approximate_amount_usd": approximate_amount_usd,
                    "token_price": price
                }

                new_contract_tx = models.ContractTransactions(**data)
                db.add(new_contract_tx)
                db.commit()
                db.refresh(new_contract_tx)
                result_list.append(new_contract_tx)
        except SQLAlchemyError as e:
            print('ERROR saving the following transaction: ' + str(data))
            print(str(e))
            continue
    return result_list

def get_last_contract_transaction(db: Session, token_symbol):
    return db.query(models.ContractTransactions).filter(
        models.ContractTransactions.token_symbol==token_symbol
    ).order_by(
        models.ContractTransactions.id.desc()).first()

def query_by_function_name(db: Session, function_name: str):
    return db.query(models.ContractTransactions).filter(
        models.ContractTransactions.function_name.match(f'{function_name}%')).order_by(
            models.ContractTransactions.id.desc()).all()

def get_transactions_by_function_name(db: Session, function_name: str = None):
    if function_name:
        result = query_by_function_name(db, function_name.value)

        return {function_name.value: result}

    result = {}
    for function_name in schemas.FunctionsName:
        data = query_by_function_name(db, function_name.value)
        result.update({
            function_name: data
        })

    return result

def get_discord_channels(db: Session):
    return db.query(models.DiscordChannels).filter_by(active=True).all()