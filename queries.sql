-- Queries do banco de dados. Apenas para referencia na hora de escrever o código

CREATE TABLE empresa (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255),
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    endereco TEXT,
    email VARCHAR(255),
    telefone VARCHAR(255)
);

CREATE TYPE periodicidade_tipo AS ENUM ('MENSAL', 'TRIMESTRAL', 'ANUAL');

CREATE TABLE obrigacao_acessoria (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    periodicidade periodicidade_tipo NOT NULL,
    empresa_id INT NOT NULL,
    FOREIGN KEY(empresa_id) REFERENCES empresa(id) ON DELETE CASCADE
);

-- -- -- CRUD EMPRESA

-- CREATE EMPRESA:
INSERT INTO empresa (nome, cnpj, endereco, email, telefone)
VALUES ('Empresa Teste', '12345678901234', 'Recife', 'empresa_teste@gmail.com', '81900000000');

-- READ EMPRESA:
SELECT * FROM empresa;
SELECT * FROM empresa WHERE cnpj = '12345678901234';
SELECT * FROM empresa WHERE id = 1;

-- UPDATE EMPRESA:
UPDATE empresa SET endereco = 'Olinda',
                   nome = 'Novo Nome',
                   email = 'empresa_novo_email@gmail.com',
                   telefone = '81900000001'
WHERE cnpj = '12345678901234';

-- DELETE EMPRESA:
DELETE FROM empresa WHERE cnpj = '12345678901234';
DELETE FROM empresa WHERE id = 1;

-- -- -- CRUD OBRIGACÕES ACESSÓRIAS

-- CREATE OBRIGACAO_ACESSORIA:
INSERT INTO obrigacao_acessoria (nome, periodicidade, empresa_id)
VALUES ('DAS', 'MENSAL', 1);

-- READ OBRIGACAO_ACESSORIA:
SELECT * FROM obrigacao_acessoria;
SELECT * FROM obrigacao_acessoria WHERE empresa_id = 1;

SELECT empresa.*, obrigacao.nome AS obrigacao, obrigacao.periodicidade
FROM empresa JOIN obrigacao_acessoria AS obrigacao
ON empresa.id = obrigacao.empresa_id;

-- UPDATE OBRIGACAO_ACESSORIA:
UPDATE obrigacao_acessoria SET nome = 'DIPJ',
                               periodicidade = 'ANUAL'
WHERE id = 2;

-- DELETE OBRIGACAO_ACESSORIA:
DELETE FROM obrigacao_acessoria WHERE id = 1;
DELETE FROM obrigacao_acessoria WHERE empresa_id = 1;
