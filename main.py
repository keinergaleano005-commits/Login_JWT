import psycopg
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from BaseModel import UsuarioCreate
from contextlib import asynccontextmanager
from fastapi import FastAPI
from db import DataBase, db
from security import  hashear_contrasena, verificar_contrasena,generar_token, obtener_usuario_actual

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(lifespan=lifespan)


@app.post("/usuarios", status_code=201)
async def crear_usuario(usuario: UsuarioCreate):
    password_hasheado = hashear_contrasena(usuario.password)
    try:
        await db.cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (usuario.nombre, usuario.email, password_hasheado),
        )
        await db.conn.commit()
    except psycopg.errors.UniqueViolation:
        await db.conn.rollback()
        raise HTTPException(status_code=400, detail="Ese correo ya está registrado")
    return {"mensaje": "Usuario creado"}

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    await db.cursor.execute(
        "SELECT id, password FROM usuarios WHERE email = %s", (form.username,)
    )
    usuario = await db.cursor.fetchone()

    if usuario is None or not verificar_contrasena(form.password, usuario[1]):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    token = generar_token(usuario[0])
    return {"access_token": token, "token_type": "bearer"}

@app.get("/perfil")
async def obtener_perfil(usuario_actual: dict = Depends(obtener_usuario_actual)):
    await db.cursor.execute(
        "SELECT id, nombre, email FROM usuarios WHERE id = %s",
        (usuario_actual["id"],),
    )
    usuario = await db.cursor.fetchone()

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id": usuario[0],
        "nombre": usuario[1],
        "email": usuario[2],
    }