from config import *
import datetime

class Users(Base):
    __tablename__ = "usuarios"
    ID = Column(Integer, primary_key = True, autoincrement = True)
    nome = Column(String(16), nullable = False)
    email = Column(String(50), nullable = False)
    senha = Column(String(50), nullable = False)

class Tokens(Base):
    __tablename__ = "tokens"
    email_usuario = Column(String(50), primary_key = True, nullable = False)
    token = Column(String(50), nullable = False)
    data_criacao = Column(DateTime, default = datetime.datetime.now)

Base.metadata.create_all(engine)