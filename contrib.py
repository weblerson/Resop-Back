from config import *
from models import User, Token

class Verify:
    @classmethod
    def password_length(cls, password: str):
        if len(password) < 8:
            return {"success": False, "response": "Senha com menos de 8 dígitos. Tente outra."}

        return {"success": True, "response": ""}

    @classmethod
    def email_not_exists(cls, email: str):
        try:
            if session.query(session.query(User).filter(User.email == email).exists()).one()[0]:
                return {"success": False, "response": "O email passado já existe."}

            return {"success": True, "response": ""}

        except:
            return {"success": False, "response": "Erro ao consultar o banco."}