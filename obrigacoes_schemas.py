from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
import empresas_schemas as schemas


class PeriodicidadeEnum(str, Enum):
    MENSAL = "MENSAL"
    TRIMESTRAL = "TRIMESTRAL"
    ANUAL = "ANUAL"


class ObrigacaoBase(BaseModel):
    nome: str
    periodicidade: PeriodicidadeEnum


class ObrigacaoUpdate(BaseModel):
    nome: Optional[str] = None
    periodicidade: Optional[PeriodicidadeEnum] = None


class ObrigacaoResponse(ObrigacaoBase):
    id: int
    empresa_id: int


class ObrigacaoJoinResponse(schemas.EmpresaResponse):
    obrigacoes: List[ObrigacaoResponse]


class SucessResponse(BaseModel):
    status: str
    data: ObrigacaoResponse


class SucessResponseDelete(BaseModel):
    status: str
    data: None


class SucessResponseMany(BaseModel):
    status: str
    data: ObrigacaoJoinResponse
