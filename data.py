from config import *
from models import Users

class Payload:
    @classmethod
    def toJSON(cls, email: str):
        try:
            user = session.query(Users).filter(Users.email == email).one()

            return {
                "success": True,
                "response": {
                    "id": user.ID,
                    "nome": user.nome,
                    "email": email
                }
            }

        except:
            return {"success": False, "response": "Ocorreu um erro ao consultar o banco."}