-- Criação do banco de dados
DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'ebenezer') THEN
        CREATE DATABASE ebenezer;
    END IF;
END
$$;

-- Conectar ao banco de dados 'ebenezer'
\c ebenezer;

-- Tabela companies
DROP TABLE IF EXISTS companies;
CREATE TABLE companies (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) DEFAULT NULL,
  cnpj VARCHAR(14) DEFAULT NULL,           -- CNPJ com 14 caracteres, sem pontos ou traços
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserção de exemplo na tabela companies
INSERT INTO companies (name, cnpj) VALUES ('Empresa Padrão', '12345678000195');

-- Tabela roles
DROP TABLE IF EXISTS roles;
CREATE TABLE roles (
  id BIGSERIAL PRIMARY KEY,
  company_id BIGINT NOT NULL,
  active BOOLEAN DEFAULT TRUE,
  description VARCHAR(255) DEFAULT NULL,
  role VARCHAR(255) DEFAULT NULL,
  FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Inserção de exemplo na tabela roles
INSERT INTO roles (company_id, active, description, role) VALUES (1, TRUE, 'Administrador', 'ADMIN');

-- Tabela users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    role_id BIGINT NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    photo BYTEA,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Inserção de exemplo na tabela users
INSERT INTO users (company_id, username, password, email, role_id, active) VALUES 
(1, 'admin', '$2a$10$St2AvRkC5G9g1R9HmNRTyuCkKyL8051CR2FGkBmpDOJaBznH7xnVK', 'admin@admin.com', 1, TRUE);

-- Tabela donors
DROP TABLE IF EXISTS donors;
CREATE TABLE donors (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL,
    person_type VARCHAR(20) NOT NULL CHECK (person_type IN ('Pessoa Física', 'Pessoa Jurídica')),
    name VARCHAR(255) NOT NULL,
    cnpj VARCHAR(30),                       -- CNPJ com 14 caracteres
    ie VARCHAR(30),
    cpf VARCHAR(30) ,                        -- CPF com 11 caracteres
    rg VARCHAR(30),
    rg_issuer VARCHAR(30),
    active BOOLEAN DEFAULT TRUE,
    user_creator_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_creator_id) REFERENCES users(id),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    -- Restrição única para (cpf, person_type)
    CONSTRAINT unique_cpf_person_type UNIQUE (cpf, person_type),
    
    -- Restrição única para (cnpj, person_type)
    CONSTRAINT unique_cnpj_person_type UNIQUE (cnpj, person_type)
);

-- Tabela donor_contacts
DROP TABLE IF EXISTS donor_contacts;
CREATE TABLE donor_contacts (
    id BIGSERIAL PRIMARY KEY,
    donor_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(60) NOT NULL,
    email VARCHAR(60),
    FOREIGN KEY (donor_id) REFERENCES donors(id) ON DELETE CASCADE,
    UNIQUE (donor_id, phone, email)  -- Restrição de unicidade para evitar duplicidade de contatos para o mesmo doador
);

-- Tabela donor_addresses
DROP TABLE IF EXISTS donor_addresses;
CREATE TABLE donor_addresses (
    id BIGSERIAL PRIMARY KEY,
    donor_id BIGINT NOT NULL,
    street VARCHAR(255) NOT NULL,
    neighborhood VARCHAR(255),
    complement VARCHAR(255),
    city VARCHAR(255) NOT NULL,
    state VARCHAR(2) NOT NULL,               -- Estado com 2 caracteres (UF)
    postal_code VARCHAR(20),                  -- CEP com 8 caracteres
    number VARCHAR(100) NOT NULL,
    country VARCHAR(60) DEFAULT 'Brazil',
    FOREIGN KEY (donor_id) REFERENCES donors(id) ON DELETE CASCADE,
    UNIQUE (donor_id)  -- Adiciona a restrição de unicidade para donor_id
);

DROP TABLE IF EXISTS agenda;
CREATE TABLE agenda (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL,
    user_creator_id BIGINT NOT NULL,
    date TIMESTAMP,
    hour VARCHAR(30),
    event_type VARCHAR(20) NOT NULL CHECK (event_type IN ('Ligação')),
    obs VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_creator_id) REFERENCES users(id),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS agenda_calls;
CREATE TABLE agenda_calls (
    id BIGSERIAL PRIMARY KEY,
    agenda_id BIGINT NOT NULL,
    donor_id BIGINT NOT NULL,
    phone VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agenda_id) REFERENCES agenda(id),
    FOREIGN KEY (donor_id) REFERENCES donors(id) ON DELETE CASCADE
);
