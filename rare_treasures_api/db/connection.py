from os import environ as env
from dotenv import load_dotenv
from pg8000.native import Connection, DatabaseError
from fastapi import HTTPException

load_dotenv()

class CreateConnection():
    ''' context manager for connection '''
    def __init__(self, prefix='PG'):
        self.connection = None
        self.prefix = prefix

    def __enter__(self):
        try:
            self.connection = Connection(
                env.get(f'{self.prefix}_USER'),
                password=env.get(f'{self.prefix}_PASSWORD'),
                database=env.get(f'{self.prefix}_DATABASE'),
                host=env.get(f'{self.prefix}_HOST'),
                port=int(env.get(f'{self.prefix}_PORT')),
                ssl_context=True
            )
            return self.connection
        except DatabaseError as exc:
            raise HTTPException(status_code=500, detail=exc) from exc

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(self.connection, Connection):
            self.connection.close()
            self.connection = None
