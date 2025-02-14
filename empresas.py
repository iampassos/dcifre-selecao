from fastapi import Depends, APIRouter, HTTPException
import database as db
import empresas_schemas as schemas
import models

router = APIRouter()


def list_empresas(db: db.Session):
    query = db.query(models.Empresa).all()

    return query


def list_empresa_by_cnpj(db: db.Session, cnpj: str, error=True):
    query = db.query(models.Empresa).filter(
        models.Empresa.cnpj == cnpj).first()

    if not query and error:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return query


def list_empresa_by_id(db: db.Session, id: int, error=True):
    query = db.query(models.Empresa).filter(
        models.Empresa.id == id).first()

    if not query and error:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return query


def add_empresa(db: db.Session, data: schemas.EmpresaBase):
    result = list_empresa_by_cnpj(db, data.cnpj, False)

    if result:
        raise HTTPException(status_code=409, detail="Empresa já existe")

    new = models.Empresa(**data.model_dump())
    db.add(new)
    db.commit()
    db.refresh(new)

    return new


def update_empresa(db: db.Session, cnpj: str, data: schemas.EmpresaUpdate):
    result = list_empresa_by_cnpj(db, cnpj)

    for key, value in data.__dict__.items():
        if value is None:
            setattr(data, key, getattr(result, key))

    data_dict = data.model_dump()
    data_dict["cnpj"] = cnpj

    db.query(models.Empresa).filter(
        models.Empresa.cnpj == cnpj).update(data_dict)
    db.commit()

    return list_empresa_by_cnpj(db, cnpj)


def delete_empresa_by_cnpj(db: db.Session, cnpj: str):
    result = list_empresa_by_cnpj(db, cnpj)

    db.delete(result)
    db.commit()


@router.get("/", response_model=schemas.SucessResponseMany, tags=["Empresas"], description="Retorna todas as empresas")
async def get_empresas(db: db.Session = Depends(db.get_db)):
    result = list_empresas(db)

    return {"status": "success", "data": result}


@router.get("/{cnpj}", response_model=schemas.SucessResponse, tags=["Empresas"], description="Retorna apenas uma empresa")
async def get_empresa(cnpj: str, db: db.Session = Depends(db.get_db)):
    result = list_empresa_by_cnpj(db, cnpj)

    return {"status": "success", "data": result}


@router.post("/", status_code=201, response_model=schemas.SucessResponse, tags=["Empresas"], description="Cria uma empresa")
async def post_empresa(data: schemas.EmpresaBase, db: db.Session = Depends(db.get_db)):
    result = add_empresa(db, data)

    return {"status": "success", "data": result}


@router.patch("/{cnpj}", response_model=schemas.SucessResponse, tags=["Empresas"], description="Altera algum dado de uma empresa")
async def patch_empresa(data: schemas.EmpresaUpdate, cnpj: str, db: db.Session = Depends(db.get_db)):
    result = update_empresa(db, cnpj, data)

    return {"status": "success", "data": result}


@router.delete("/{cnpj}", response_model=schemas.SucessResponseDelete, tags=["Empresas"], description="Deleta uma empresa")
async def delete_empresa(cnpj: str, db: db.Session = Depends(db.get_db)):
    delete_empresa_by_cnpj(db, cnpj)

    return {"status": "success", "data": None}
