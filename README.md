API Simples para a seleção do estágio.

Não foi especificado qual biblioteca utilizar para os testes, então decidi usar o pytest.
Também  não foi especificado qual biblioteca para a migração, então fiz tanto o sql puro quanto
a biblioteca alembic.
Utilizei a biblioteca uvicorn para rodar o servidor. http://localhost:8000/docs contém os docs em swagger

OBS: migracao.py é uma alteração do arquivo gerado pelo alembic em uma subpasta

PASSO A PASSO:
1. [X] Modelar o banco de dados no sql puro
2. [X] Criar todas as queries no sql puro
3. [X] Migração
4. [X] Converter as queries no sql puro para SQLAlchemy
5. [X] Criar Pydantic Models
6. [X] Criar API com FastAPI
7. [X] Validação de entrada com Pydantic
8. [X] Validação de saída com Pydantic
9. [X] Testes unitários com pytest
10. [X] Documentação
11. [X] README com as informações
