-- Criação do banco de dados
DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'ebenezer') THEN
        CREATE DATABASE ebenezer;
    END IF;
END
$$;

-- Agora conecte-se ao banco de dados 'ebenezer'
\c ebenezer;

-- Tabela companies
DROP TABLE IF EXISTS companies;
CREATE TABLE companies (
  id BIGSERIAL PRIMARY KEY,                -- ID único da empresa
  name VARCHAR(255) DEFAULT NULL,
  cnpj VARCHAR(14) DEFAULT NULL,           -- Considerando um CNPJ de 14 caracteres
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Data de criação
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Data de atualização
);

-- Inserção de exemplo na tabela companies
INSERT INTO companies (name, cnpj) VALUES ('Empresa Padrão', '12345678000195');

-- Tabela roles
DROP TABLE IF EXISTS roles;
CREATE TABLE roles (
  id BIGSERIAL PRIMARY KEY,                -- ID único da função
  company_id BIGINT NOT NULL,              -- Relacionamento com a empresa
  active BOOLEAN DEFAULT TRUE,
  description VARCHAR(255) DEFAULT NULL,
  role VARCHAR(255) DEFAULT NULL,
  FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE  -- Definindo relacionamento com companies
);

-- Inserção de exemplo na tabela roles
INSERT INTO roles (company_id, active, description, role) VALUES (1, TRUE, 'Administrador', 'ADMIN');

-- Tabela users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,               -- ID único do usuário
    company_id BIGINT NOT NULL,             -- Mantém NOT NULL
    username VARCHAR(255) NOT NULL,         -- Nome de usuário
    password VARCHAR(255) NOT NULL,         -- Senha
    email VARCHAR(255),                     -- E-mail
    role_id BIGINT NOT NULL,                -- Relacionamento com a função
    active BOOLEAN DEFAULT TRUE,            -- Status de atividade
    photo BYTEA,                            -- Foto do usuário (tipo binário)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,  -- Altera para `ON DELETE CASCADE`
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Inserção de exemplo na tabela users
INSERT INTO users (company_id, username, password, email, role_id, active) VALUES 
(1, 'admin', '$2a$10$St2AvRkC5G9g1R9HmNRTyuCkKyL8051CR2FGkBmpDOJaBznH7xnVK', 'admin@admin.com', 1, TRUE);

-- Tabela donors
DROP TABLE IF EXISTS donors;
CREATE TABLE donors (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL,            -- Foreign key to companies
    name VARCHAR(255) NOT NULL,            -- Donor name
    cnpj VARCHAR(20),                      -- CNPJ for business donors
    ie VARCHAR(20),                        -- State registration number (IE)
    cpf VARCHAR(20),                       -- CPF for individual donors
    rg VARCHAR(20),                        -- RG (identity) number
    rg_issuer VARCHAR(20),                 -- Issuing organization for RG
    active BOOLEAN DEFAULT TRUE,           -- Active status
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_creator_id BIGINT,                -- Foreign key to user who created the entry
    FOREIGN KEY (user_creator_id) REFERENCES users(id),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Tabela donor_contacts
DROP TABLE IF EXISTS donor_contacts;
CREATE TABLE donor_contacts (
    id BIGSERIAL PRIMARY KEY,
    donor_id BIGINT NOT NULL,              -- Foreign key to donors
    contact_name VARCHAR(255),             -- Contact person name
    phone_number VARCHAR(20),              -- Phone number of the donor or contact person
    FOREIGN KEY (donor_id) REFERENCES donors(id) ON DELETE CASCADE
);

-- Tabela donor_addresses
DROP TABLE IF EXISTS donor_addresses;
CREATE TABLE donor_addresses (
    id BIGSERIAL PRIMARY KEY,
    donor_id BIGINT NOT NULL,              -- Foreign key to link to a donor
    street VARCHAR(255) NOT NULL,          -- Street name
    neighborhood VARCHAR(255),             -- Neighborhood
    complement VARCHAR(255),               -- Address complement
    city VARCHAR(255) NOT NULL,            -- City
    state VARCHAR(255) NOT NULL,           -- State
    postal_code VARCHAR(10),               -- Postal code (CEP)
    country VARCHAR(50) DEFAULT 'Brazil',  -- Country, default to Brazil
    FOREIGN KEY (donor_id) REFERENCES donors(id) ON DELETE CASCADE
);

-- Inserção de exemplo na tabela donors
INSERT INTO donors (company_id, name, cnpj, ie, cpf, rg, rg_issuer, active, user_creator_id)
VALUES 
    (1, 'John Doe', NULL, NULL, '123.456.789-00', 'MG-12.345.678', 'SSP', TRUE, 1),
    (1, 'Jane Smith', NULL, NULL, '987.654.321-00', 'SP-98.765.432', 'SSP', TRUE, 1),
    (1, 'ACME Corporation', '12.345.678/0001-99', '123456789', NULL, NULL, NULL, TRUE, 1);

-- Inserção de exemplo na tabela donor_contacts
INSERT INTO donor_contacts (donor_id, contact_name, phone_number)
VALUES
    (1, 'John Doe', '+55 11 98765-4321'),
    (2, 'Jane Smith', '+55 21 12345-6789'),
    (3, 'Maria Lopez', '+55 31 34567-8901');  -- Contact for ACME Corporation

-- Inserção de exemplo na tabela donor_addresses
INSERT INTO donor_addresses (donor_id, street, neighborhood, complement, city, state, postal_code, country)
VALUES
    (1, '123 Elm St', 'Downtown', 'Apt 45', 'São Paulo', 'SP', '01001-000', 'Brazil'),
    (2, '456 Oak Ave', 'Central Park', NULL, 'Rio de Janeiro', 'RJ', '20001-000', 'Brazil'),
    (3, '789 Maple Dr', 'Industrial Area', 'Suite 100', 'Belo Horizonte', 'MG', '30001-000', 'Brazil');
