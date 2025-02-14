from fastapi import FastAPI
import empresas
import obrigacoes

app = FastAPI()

app.include_router(empresas.router, prefix="/api/empresas")
app.include_router(obrigacoes.router, prefix="/api/obrigacoes")
