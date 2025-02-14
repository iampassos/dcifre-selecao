from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, constr
from typing import Optional
import database as db
import models

router = APIRouter()


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


def list_empresas(db: db.Session):
    query = db.query(models.Empresa).all()

    return query


def list_empresa_by_cnpj(db: db.Session, cnpj: str, error=True):
    query = db.query(models.Empresa).filter(
        models.Empresa.cnpj == cnpj).first()

    if not query and error:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return query


def add_empresa(db: db.Session, data: EmpresaBase):
    result = list_empresa_by_cnpj(db, data.cnpj, False)

    if result:
        raise HTTPException(status_code=409, detail="Empresa já existe")

    new = models.Empresa(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)

    return new


def update_empresa(db: db.Session, cnpj: str, data: EmpresaUpdate):
    result = list_empresa_by_cnpj(db, cnpj)

    for key, value in data.__dict__.items():
        if value is None:
            setattr(data, key, getattr(result, key))

    data_dict = data.dict()
    data_dict["cnpj"] = cnpj

    db.query(models.Empresa).filter(
        models.Empresa.cnpj == cnpj).update(data_dict)
    db.commit()

    return list_empresa_by_cnpj(db, cnpj)


def delete_empresa_by_cnpj(db: db.Session, cnpj: str):
    result = list_empresa_by_cnpj(db, cnpj)

    db.delete(result)
    db.commit()


@router.get("/")
async def get_empresas(db: db.Session = Depends(db.get_db)):
    result = list_empresas(db)

    return {"status": "success", "data": result}


@router.get("/{cnpj}")
async def get_empresa(cnpj: str, db: db.Session = Depends(db.get_db)):
    result = list_empresa_by_cnpj(db, cnpj)

    return {"status": "success", "data": result}


@router.post("/")
async def post_empresa(data: EmpresaBase, db: db.Session = Depends(db.get_db)):
    result = add_empresa(db, data)

    return {"status": "success", "data": result}


@router.patch("/{cnpj}")
async def patch_empresa(data: EmpresaUpdate, cnpj: str, db: db.Session = Depends(db.get_db)):
    result = update_empresa(db, cnpj, data)

    return {"status": "success", "data": result}


@router.delete("/{cnpj}")
async def delete_empresa(cnpj: str, db: db.Session = Depends(db.get_db)):
    delete_empresa_by_cnpj(db, cnpj)

    return {"status": "success", "data": None}
