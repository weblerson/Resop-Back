from config import *

class User(Base):
    __tablename__ = "usuarios"
    ID = Column(Integer, primary_key = True, autoincrement = True)
    nome = Column(String(16), nullable = False)
    email = Column(String(50), nullable = False)
    senha = Column(String(50), nullable = False)

class Token(Base):
    __tablename__ = "token"
    user_email = Column(String(50), primary_key = True, nullable = False)
    token = Column(String(50), nullable = False)

Base.metadata.create_all(engine)