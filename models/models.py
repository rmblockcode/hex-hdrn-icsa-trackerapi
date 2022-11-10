from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from datetime import datetime
from .database import Base

class TimeStampMixin(object):
    create_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now())


class ContractTransactions(TimeStampMixin, Base):
    __tablename__ = "contract_transactions"

    id = Column(Integer, primary_key=True, index=True)
    token_symbol = Column(String, index=True)
    block_number = Column(String)
    tx_timestamp = Column(String)
    hash = Column(String)
    nonce = Column(String)
    block_hash = Column(String)
    transaction_index = Column(String)
    tx_from = Column(String)
    tx_to = Column(String)
    value = Column(String)
    gas = Column(String)
    gas_price = Column(String)
    is_error = Column(String)
    txreceipt_status = Column(String)
    input = Column(String)
    contract_address = Column(String)
    cumulative_gas_used = Column(String)
    gas_used = Column(String)
    confirmations = Column(String)
    method_id = Column(String)
    function_name = Column(String, index=True)
    amount = Column(String)
    approximate_amount_usd = Column(Float)
    token_price = Column(Float)


class DiscordChannels(Base):
    __tablename__ = "discord_channels"
    id = Column(Integer, primary_key=True, index=True)
    channel_unique_name = Column(String)
    webhook_url = Column(String)
    active = Column(Boolean, default=True)
