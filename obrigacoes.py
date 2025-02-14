from fastapi import Depends, APIRouter, HTTPException
import database as db
import obrigacoes_schemas as schemas
import empresas
import models


router = APIRouter()


def list_obrigacao_by_id(db: db.Session, id: int):
    query = db.query(models.ObrigacaoAcessoria).filter(
        models.ObrigacaoAcessoria.id == id).first()

    if not query:
        raise HTTPException(
            status_code=404, detail="Obrigação acessória não encontrada")

    return query


def list_obrigacoes_by_cnpj(db: db.Session, cnpj: str):
    empresas.list_empresa_by_cnpj(db, cnpj)

    query = db.query(
        models.Empresa,
        models.ObrigacaoAcessoria
    ).join(
        models.ObrigacaoAcessoria,
        models.Empresa.id == models.ObrigacaoAcessoria.empresa_id
    ).filter(models.Empresa.cnpj == cnpj).all()

    if len(query) == 0:
        raise HTTPException(
            status_code=404, detail="Obrigações acessórias não encontradas")

    empresa = []
    obrigacoes = []

    for row in query:
        if len(empresa) == 0:
            empresa_dict = row.Empresa.__dict__
            empresa.append(empresa_dict)

        obrigacao_dict = row.ObrigacaoAcessoria.__dict__
        obrigacoes.append(obrigacao_dict)

    return {**empresa[0], "obrigacoes": obrigacoes}


def list_obrigacao(db: db.Session, cnpj: str, id: int):
    empresa = empresas.list_empresa_by_cnpj(db, cnpj)
    obrigacao = list_obrigacao_by_id(db, id)

    if empresa.id != obrigacao.empresa_id:
        raise HTTPException(
            status_code=404, detail="Obrigaçã̇o acessória não encontrada")

    return obrigacao


def add_obrigacao_by_cnpj(db: db.Session, cnpj: str, data: schemas.ObrigacaoBase):
    result = empresas.list_empresa_by_cnpj(db, cnpj)

    data_dict = data.dict()
    data_dict["empresa_id"] = result.id

    new = models.ObrigacaoAcessoria(**data_dict)
    db.add(new)
    db.commit()
    db.refresh(new)

    result = list_obrigacao_by_id(db, new.id)

    return result


def update_obrigacao(db: db.Session, id: int, data: schemas.ObrigacaoUpdate):
    result = list_obrigacao_by_id(db, id)

    for key, value in data.__dict__.items():
        if value is None:
            setattr(data, key, getattr(result, key))

    data_dict = data.dict()
    data_dict["id"] = id
    data_dict["empresa_id"] = result.empresa_id

    db.query(models.ObrigacaoAcessoria).filter(
        models.ObrigacaoAcessoria.id == id).update(data_dict)
    db.commit()

    return list_obrigacao_by_id(db, id)


def delete_obrigacao_by_id(db: db.Session, id: int):
    result = list_obrigacao_by_id(db, id)

    db.delete(result)
    db.commit()


@router.get("/{cnpj}/{id}", response_model=schemas.SucessResponse, tags=["Obrigações"], description="Retorna uma obrigação de uma empresa")
async def get_obrigacao(cnpj: str, id: int, db: db.Session = Depends(db.get_db)):
    result = list_obrigacao(db, cnpj, id)

    return {"status": "success", "data": result}


@router.get("/{cnpj}", response_model=schemas.SucessResponseMany, tags=["Obrigações"], description="Retorna as obrigações de apenas uma empresa")
async def get_obrigacoes_empresa(cnpj: str, db: db.Session = Depends(db.get_db)):
    result = list_obrigacoes_by_cnpj(db, cnpj)

    return {"status": "success", "data": result}


@router.post("/{cnpj}", status_code=201, response_model=schemas.SucessResponse, tags=["Obrigações"], description="Adiciona uma obrigação a uma empresa")
async def post_obrigacao(data: schemas.ObrigacaoBase, cnpj: str, db: db.Session = Depends(db.get_db)):
    result = add_obrigacao_by_cnpj(db, cnpj, data)

    return {"status": "success", "data": result}


@router.patch("/{id}", response_model=schemas.SucessResponse, tags=["Obrigações"], description="Altera um dado de uma obrigação")
async def patch_obrigacao(data: schemas.ObrigacaoUpdate, id: int, db: db.Session = Depends(db.get_db)):
    result = update_obrigacao(db, id, data)

    return {"status": "success", "data": result}


@router.delete("/{id}", response_model=schemas.SucessResponseDelete, tags=["Obrigações"], description="Deleta uma obrigação de uma empresa")
async def delete_obrigacao(id: int, db: db.Session = Depends(db.get_db)):
    delete_obrigacao_by_id(db, id)

    return {"status": "success", "data": None}
