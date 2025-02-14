from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    nome = Column(String(255))
    cnpj = Column(String(14), nullable=False, unique=True)
    endereco = Column(Text())
    email = Column(String(255))
    telefone = Column(String(255))

    obrigacoes = relationship("ObrigacaoAcessoria",
                              backref="empresa", cascade="all, delete")


class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacao_acessoria"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    nome = Column(Text(), nullable=False)
    periodicidade = Column(
        Enum("MENSAL", "TRIMESTRAL", "ANUAL", name="periodicidade_tipo"), nullable=False)
    empresa_id = Column(Integer(), ForeignKey("empresa.id"), nullable=False)
