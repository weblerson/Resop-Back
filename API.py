from config import *
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from models import Users, Tokens
import bcrypt
from contrib import Verify, Token

class User(BaseModel):
    ID: Optional[int]
    nome: Optional[str]
    email: Optional[str]
    senha: Optional[str]
    token: Optional[str]

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
    user_exists = Verify.user_credentials(f"{user.email}@lerson.com", user.senha)
    user_have_token = Token.verify_user_token(email = f"{user.email}@lerson.com")

    if user_exists["success"]:
        if user_have_token["success"]:
            token_is_not_expired = Token.verify_token(token = user_have_token["response"])

            if token_is_not_expired["success"]:
                #final
                return {"success": True, "response": token_is_not_expired["response"]}

            else:
                new_token = Token.update(email = f"{user.email}@lerson.com")
                if new_token["success"]:
                    #final
                    return {"success": True, "response": new_token["response"]}

                return {"success": False, "response": new_token["response"]}

        else:
            created_token = Token.create(email = f"{user.email}@lerson.com")
            if created_token["success"]:
                #final
                return {"success": True, "response": created_token["response"]}

            return {"success": False, "response": created_token["response"]}

    return {"success": False, "response": user_exists["response"]}
