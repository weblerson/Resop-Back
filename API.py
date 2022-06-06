from config import *
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from models import Users, Tokens
import bcrypt
from contrib import Verify

class User(BaseModel):
    ID: Optional[int]
    nome: str
    email: str
    senha: Optional[str]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.post("/register")
def register(user: User):
    email_not_exists = Verify.email_not_exists(email = f"{user.email}@lerson.com")
    password_strong = Verify.password_length(password = user.senha)

    if not password_strong["success"]:
        return password_strong

    if email_not_exists["success"] and password_strong["success"]:
        b_pass = user.senha.encode()
        h_pass = bcrypt.hashpw(b_pass, bcrypt.gensalt())

        session.add(Users(nome = user.nome, email = f"{user.email}@lerson.com", senha = h_pass.decode()))
        session.commit()

        return {"success": True, "response": "Usuário cadastrado com sucesso!"}

    else:
        return email_not_exists

@app.post("/login")
def login(user: User):
    pass