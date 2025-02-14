from fastapi import FastAPI
import empresas
import obrigacoes

app = FastAPI(
    title="API Simples dcifre",
    description="API básico para a seleção de estágio da dcifre",
    version="1.0.0",
)

app.include_router(empresas.router, prefix="/api/empresas")
app.include_router(obrigacoes.router, prefix="/api/obrigacoes")

app.openapi_tags = [
    {
        "name": "Empresas",
        "description": "API para gerenciamento de empresas na dcifre",
    },
    {
        "name": "Obrigações",
        "description": "API para gerenciamento das obrigações acessórias das empresas na dcifre",
    },
]
