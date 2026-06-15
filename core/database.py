from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


POSTGESQL_DATABASE_URL = "postgesql+asyncpg://postgres:postgres@localhost/todoAppdatabase"


engine = create_engine(POSTGESQL_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Person (Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

