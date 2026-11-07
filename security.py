import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

CLAVE_SECRETA = os.getenv("JWT_SECRET_CODE")
if CLAVE_SECRETA is None:
    raise RuntimeError("Falta JWT_SECRET_CODE en el .env")

ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hashear_contrasena(contrasena: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(contrasena.encode("utf-8"), salt).decode("utf-8")


def verificar_contrasena(contrasena: str, hash_guardado: str) -> bool:
    return bcrypt.checkpw(
        contrasena.encode("utf-8"),
        hash_guardado.encode("utf-8"),
    )


def generar_token(id_usuario: int) -> str:
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    payload = {"id": id_usuario, "exp": expiracion}
    return jwt.encode(payload, CLAVE_SECRETA, algorithm=ALGORITMO)


def verificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> dict:
    return verificar_token(token)