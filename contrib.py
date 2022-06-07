import os
from config import *
from models import Users, Tokens
from data import Payload
import jwt
from cryptography.hazmat.primitives import serialization

class Verify:
    @staticmethod
    def password_length(password: str):
        if len(password) < 8:
            return {"success": False, "response": "Senha com menos de 8 dígitos. Tente outra."}

        return {"success": True, "response": ""}

    @staticmethod
    def email_not_exists(email: str):
        try:
            if session.query(session.query(Users).filter(Users.email == email).exists()).one()[0]:
                return {"success": False, "response": "O email passado já existe."}

            return {"success": True, "response": ""}

        except:
            return {"success": False, "response": "Erro ao consultar o banco."}

class Token:
    @staticmethod
    def create(email: str):
        private_key = open(os.path.join(".ssh", "id_rsa")).read()
        key = serialization.load_ssh_private_key(private_key.encode(), password = b"")

        payload_data = Payload.toJSON(email = email)
        if payload_data["success"]:
            token = jwt.encode(payload = payload_data["response"], key = key, algorithm = "RS256")

            return {"success": True, "response": token}

        return payload_data

    @staticmethod
    def verify(token: str):
        public_key = open(os.path.join(".ssh", "id_rsa.pub")).read()
        key = serialization.load_ssh_public_key(public_key.encode())

        decoded = jwt.decode(token, key = key, algorithms = ["RS256"])
        