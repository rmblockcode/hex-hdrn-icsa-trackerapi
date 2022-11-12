# hex-hdrn-icsa-trackerapi

## Environment Variables:

    export ETHERSCAN_API_KEY={ETHERSCAN_API_KEY}
    export ETHERSCAN_API_URL=https://api.etherscan.io/api
    export SQLALCHEMY_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/token_trackerdb
    export COINGECKO_API=https://api.coingecko.com/api/v3/

    # API URL: For crontab purpose
    export API_URL=http://127.0.0.1:8001/


### Execute Migrations:

    Only execute the following command if it is the first time:
    > alembic init alembic

    In order to generate migration file version execute:
    > alembic revision --autogenerate -m "ADD SHORT MESSAGE HERE"

    Execute migrations:
    > alembic upgrade head


## Prepare crontab every minute in order to get new transactions:

```
curl -X 'GET' 'http://{URL_API}/transaction_list/icsa' -H 'accept: application/json'
```


## Create discord settings in discord_channel table:

1. In discord create two channels: an icosa and hedron channels.
    
2. Copy webhook url and continue the next step.

3. In database create two rows with the following information:

* Create a row with channel_unique_name: icosa-channel
* Create a row with channel_unique_name: hedron-channel
        
In both cases, add each webhook url created in step 2.

## Execute project locally:

```
uvicorn main:app [--port {CUSTOM_PORT}] [--reload]
```