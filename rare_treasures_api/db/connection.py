''' Database connection module '''
from os import environ as env
from dotenv import load_dotenv
from pg8000.native import Connection, DatabaseError
from fastapi import HTTPException
from ..dependencies import root_dir

APP_ENV = env.get('APP_ENV', default='test')
load_dotenv(f'{root_dir}/.env.{APP_ENV}')

print(f'\nAPP_ENV: {APP_ENV}')

class CreateConnection():
    ''' context manager for connection '''
    def __init__(self):
        self.connection = None

    def __enter__(self):
        try:
            self.connection = Connection(
                env.get('PG_USER'),
                password=env.get('PG_PASSWORD'),
                database=env.get('PG_DATABASE'),
                host=env.get('PG_HOST'),
                port=int(env.get('PG_PORT')),
                ssl_context=env.get('PG_SSL_CONTEXT', False)
            )
            return self.connection
        except DatabaseError as exc:
            raise HTTPException(status_code=500, detail=exc) from exc

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(self.connection, Connection):
            self.connection.close()
            self.connection = None
