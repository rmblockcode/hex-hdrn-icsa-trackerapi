# hex-hdrn-icsa-trackerapi

Execute Migrations

    Only execute the following command if it is the first time:
    > alembic init alembic

    In order to generate migration file version execute:
    > alembic revision --autogenerate -m "ADD SHORT MESSAGE HERE"

    Execute migrations:
    > alembic upgrade head