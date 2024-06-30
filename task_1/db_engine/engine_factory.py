from abc import ABC, abstractmethod
from typing import Literal, Union

from sqlalchemy import create_engine, text

DB_TYPE = Literal["postgres", "sqlite"]


class AbstractEngine(ABC):
    def __init__(self, echo: bool = False):
        self.echo = echo

    @abstractmethod
    def create(self):
        raise NotImplementedError


class PostgresEngine(AbstractEngine):
    def __init__(self, user: str, password: str, host: str, port: Union[int, str], db: str, echo: bool):
        super().__init__(echo)
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db

    def create(self):
        engine = create_engine(
            f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}",
            echo=self.echo
        )
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{self.db}'"))
            exists = result.scalar()
            if not exists:
                conn.execute(text(f'CREATE DATABASE {self.db}'))

        return create_engine(f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}")


class SQLiteEngine(AbstractEngine):
    def __init__(self, path: str, db: str, echo: bool):
        super().__init__(echo)
        self.db = db
        self.path = path

    def create(self):
        engine = create_engine(
            f"sqlite:///{self.path}",
            echo=self.echo
        )
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.db}"))
        return create_engine(f"sqlite:///{self.path}/{self.db}", echo=self.echo)


class DBEngineFactory:
    @classmethod
    def get_engine(cls, db_type: DB_TYPE, **kwargs):
        if db_type == "postgres":
            return PostgresEngine(**kwargs).create()
        elif db_type == "sqlite":
            return SQLiteEngine(**kwargs).create()
        else:
            raise ValueError("Invalid db type")
