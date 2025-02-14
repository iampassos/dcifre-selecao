from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List


class EmpresaBase(BaseModel):
    nome: str
    cnpj: constr(max_length=14)
    endereco: str
    email: EmailStr
    telefone: str


class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None


class EmpresaResponse(EmpresaBase):
    id: int


class SucessResponse(BaseModel):
    status: str
    data: EmpresaResponse


class SucessResponseDelete(BaseModel):
    status: str
    data: None


class SucessResponseMany(BaseModel):
    status: str
    data: List[EmpresaResponse]
