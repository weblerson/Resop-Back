from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CONN = "sqlite:///users.db"

engine = create_engine(CONN, echo = False)
Session = sessionmaker(bind = engine)
session = Session()
Base = declarative_base()