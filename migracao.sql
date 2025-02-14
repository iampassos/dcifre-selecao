-- Migração no SQL puro caso vocês prefiram.

DROP TABLE IF EXISTS obrigacao_acessoria CASCADE;
DROP TYPE IF EXISTS periodicidade_tipo;
DROP TABLE IF EXISTS empresa CASCADE;

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

