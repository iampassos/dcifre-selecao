"""criar tabelas do banco de dados

Revision ID: 572e9a7f89d1
Revises:
Create Date: 2025-02-13 19:42:37.039025

"""


from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey


# revision identifiers, used by Alembic.
revision: str = "572e9a7f89d1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# IMPORTANTE:
# Não foi especificado qual tipo de migração vocês queriam, então eu assumi
# que fosse um script simples como esse em alembic.
# Eu iria fazer o script no SQL puro, mas como ficou ambíguo a questão, decidi que
# o alembic seria mais provável de ser a resposta correta. Acabei fazendo os dois.


def upgrade():
    op.create_table(
        "empresa",
        Column("id", Integer(), primary_key=True, autoincrement=True),
        Column("nome", String(255)),
        Column("cnpj", String(14), nullable=False, unique=True),
        Column("endereco", Text()),
        Column("email", String(255)),
        Column("telefone", String(255))
    )

    op.create_table(
        "obrigacao_acessoria",
        Column("id", Integer(), primary_key=True, autoincrement=True),
        Column("nome", Text(), nullable=False),
        Column("periodicidade", Enum("MENSAL", "TRIMESTRAL", "ANUAL", name="periodicidade_tipo"),
               nullable=False),
        Column("empresa_id", Integer(),
               ForeignKey("empresa.id", ondelete="CASCADE"), nullable=False)
    )


def downgrade():
    op.drop_table("obrigacao_acessoria")
    op.drop_table("empresa")
