from pydantic import BaseModel, Field

class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=11, max_length=40)
    password: str = Field(min_length=2, max_length=40)