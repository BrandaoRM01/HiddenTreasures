CREATE DATABASE IF NOT EXISTS pontos_turisticos;

USE pontos_turisticos;

CREATE TABLE IF NOT EXISTS usuarios (
    email VARCHAR(150) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    url_foto VARCHAR(500) DEFAULT 'img/default/user_foto.webp',
    tipo_usuario ENUM('user', 'admin', 'superadmin') DEFAULT 'user' NOT NULL,
    token_recuperacao VARCHAR(255) NULL,
    token_expiracao DATETIME NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS historico_senhas (
    usuario_email VARCHAR(255) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (usuario_email, senha_hash),
    FOREIGN KEY (usuario_email) REFERENCES usuarios(email) 
    ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS promocoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    desconto DECIMAL(5,2) NOT NULL CHECK (desconto > 0 AND desconto <= 100),
    data_inicio DATE,
    data_fim DATE,
    CHECK (data_fim IS NULL OR data_fim >= data_inicio)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pontos_turisticos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL UNIQUE,
    localizacao VARCHAR(150) NOT NULL,
    descricao TEXT NOT NULL,
    horario_funcionamento VARCHAR(100),
    custo_entrada DECIMAL(10,2) DEFAULT 0.00,
    url_imagem VARCHAR(500) DEFAULT 'img/default/hidden_treasures_logo.png',
    categoria_id INT NOT NULL,
    promocao_id INT DEFAULT NULL,

    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    ON DELETE CASCADE,
    FOREIGN KEY (promocao_id) REFERENCES promocoes(id)
    ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS avaliacoes (
    usuario_email VARCHAR(150) NOT NULL,
    ponto_id INT NOT NULL,
    nota INT NOT NULL CHECK (nota >= 1 AND nota <= 5),
    comentario TEXT,
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (usuario_email, ponto_id),
    FOREIGN KEY (usuario_email) REFERENCES usuarios(email)
    ON DELETE CASCADE,
    FOREIGN KEY (ponto_id) REFERENCES pontos_turisticos(id)
    ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS favoritos (
    usuario_email VARCHAR(150) NOT NULL,
    ponto_id INT NOT NULL,

    PRIMARY KEY (usuario_email, ponto_id),

    FOREIGN KEY (usuario_email) REFERENCES usuarios(email)
    ON DELETE CASCADE,

    FOREIGN KEY (ponto_id) REFERENCES pontos_turisticos(id)
    ON DELETE CASCADE
) ENGINE=InnoDB;