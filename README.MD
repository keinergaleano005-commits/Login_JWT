# Login JWT con FastAPI

API de autenticación con registro y login de usuarios usando JWT, más un frontend sencillo que inicia sesión y consume una ruta protegida. El servidor es *stateless*: no guarda sesiones, solo verifica el token que el cliente envía en cada petición.

## Qué hace

- Registra usuarios guardando la contraseña como hash.
- Valida credenciales en el login y devuelve un token con expiración de 30 minutos.
- Protege rutas: solo responden si llega un token válido.
- Devuelve errores HTTP claros (400 correo duplicado, 401 credenciales o token inválidos).
- Incluye un frontend que guarda el token y muestra el id del usuario autenticado.

## Tecnologías

- FastAPI y Uvicorn
- PostgreSQL con psycopg 3 (asíncrono)
- JWT con PyJWT
- bcrypt para el hash de contraseñas
- Pydantic para la validación
- HTML, CSS y JavaScript para el frontend