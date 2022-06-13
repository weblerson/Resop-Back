from config import *
from models import Users, Tokens
from data import Payload
import bcrypt
import datetime
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

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

    @staticmethod
    def user_credentials(email: str, password: str):
        if session.query(session.query(Users).filter(Users.email == email).exists()).one()[0]:
            user = session.query(Users).filter(Users.email == email).one()

            if bcrypt.checkpw(password.encode(), user.senha.encode()):
                return {"success": True, "response": ""}

            return {"success": False, "response": "A senha passada está incorreta."}

        return {"success": False, "response": "O endereço de email passado não existe."}

    @staticmethod
    def user_token(email: str, token: str):
        if session.query(session.query(Tokens).filter(Tokens.token == token).exists()).one()[0]:
            token = session.query(Tokens).filter(Tokens.token == token).one()
            user = session.query(Users).filter(Users.email == token.email_usuario).one()

            try:
                decoded = jwt.decode(token, key = user.public_key, algorithms = ["RS256"])

                if decoded["email"] == email:
                    #Autoriza ação
                    return {"success": True, "response": ""}

                else:
                    #Nega ação
                    return {"success": False, "response": ""}

            except:
                return {"success": False, "response": ""}

class Keys:
    @staticmethod
    def generate_keys():
        key = rsa.generate_private_key(
            backend = default_backend(),
            public_exponent = 65537,
            key_size = 2048
        )

        private_key = key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        )

        public_key = key.public_key().public_bytes(
            serialization.Encoding.OpenSSH,
            serialization.PublicFormat.OpenSSH
        )

        return private_key, public_key

class Token:
    @staticmethod
    def create(email: str):
        private_key, public_key = Keys.generate_keys()

        payload_data = Payload.toJSON(email = email)
        if payload_data["success"]:
            token = jwt.encode(payload = payload_data["response"], key = private_key, algorithm = "RS256")

            try:
                session.add(Tokens(
                    email_usuario = email,
                    token = token,
                    public_key = public_key
                ))

                session.commit()

                return {"success": True, "response": token}

            except:
                return {"success": False, "response": "Ocorreu um erro ao se comunicar com o banco"}

        else:
            return {"success": False, "response": payload_data["response"]}

    @staticmethod
    def update(email: str):
        try:
            private_key, public_key = Keys.generate_keys()
            payload_data = Payload.toJSON(email = email)

            if payload_data["success"]:
                token = jwt.encode(payload = payload_data, key = private_key, algorithm = "RS256")

                session.query(Tokens).filter(Tokens.email_usuario == email).update({
                    "token": token,
                    "data_criacao": datetime.datetime.now(),
                    "public_key": public_key
                })

                session.commit()

                return {"success": True, "response": token}

        except:
            return {"success": False, "response": "Ocorreu um erro ao consultar o banco."}

    @staticmethod
    def verify_token(token: str):
        if session.query(session.query(Tokens).filter(Tokens.token == token).exists()).one()[0]:
            user_data = session.query(Tokens).filter(Tokens.token == token).one()
            date_now = datetime.datetime.now()

            interval = date_now.date() - user_data.data_criacao.date()

            #interval.days
            if interval.days < 15:
                return {"success": True, "response": token}

            return {"success": False, "response": ""}

    @staticmethod
    def verify_user_token(email: str):
        if session.query(session.query(Tokens).filter(Tokens.email_usuario == email).exists()).one()[0]:
            user = session.query(Tokens).filter(Tokens.email_usuario == email).one()

            return {"success": True, "response": user.token}

        return {"success": False, "response": ""}
        