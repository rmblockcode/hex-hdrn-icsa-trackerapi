import discord_notify as dn
from sqlalchemy.orm import Session

from models.crud import get_discord_channels

def discord_notifications(db: Session, new_transactions):
    # Getting discord channels active
    discord_channels = get_discord_channels(db)
    counter_icosa = 0
    counter_hedron = 0
    if new_transactions:
        message_icosa = ""
        message_hedron = ""
        for transaction in new_transactions:
            message = \
                f'{transaction.function_name} | ' + \
                f'Amount: {transaction.amount} | ' + \
                f'Approx. amount in USD: {transaction.approximate_amount_usd}\n\n'

            # message = f'''Function name: {transaction.function_name}\n
            #     Amount: {transaction.amount}\n
            #     Approximate amount in USD: {transaction.approximate_amount_usd}\n
            #     ---------------------------------------------------\n\n
            # '''

            if transaction.function_name.startswith('icsa'):
                counter_icosa += 1
                message_icosa += message
            elif transaction.function_name.startswith('hdrn') or \
                transaction.function_name.startswith('loanLiquidateBid'):
                counter_hedron += 1
                message_hedron += message

        for channel in discord_channels:
            message_counter_icosa = \
                f'''\n-----------------------------
                New Transactions Alert: {counter_icosa} transactions\n'''
            message_counter_hedron = \
                f'''\n-----------------------------
                New Transactions Alert: {counter_hedron} transactions \n'''
            
            notifier = dn.Notifier(channel.webhook_url)
            if channel.channel_unique_name == 'icosa-channel':    
                notifier.send(
                    message_counter_icosa + message_icosa,
                    print_message=False
                )
            elif channel.channel_unique_name == 'hedron-channel':    
                notifier.send(
                    message_counter_hedron + message_hedron,
                    print_message=False
                )
