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

CREATE TABLE IF NOT EXISTS ecossistemas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tipos_culturais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pontos_turisticos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL UNIQUE,
    localizacao VARCHAR(150) NOT NULL,
    descricao TEXT NOT NULL,
    horario_funcionamento VARCHAR(100),
    custo_entrada DECIMAL(10,2) DEFAULT 0.00,
    url_imagem VARCHAR(500) DEFAULT 'img/default/hidden_treasures_logo.png',
    area_km2 FLOAT,
    ano_fundacao VARCHAR(100),
    tipo_ponto ENUM('natural', 'cultural') NOT NULL,
    status ENUM('rejeitado', 'pendente', 'aprovado') NOT NULL DEFAULT 'pendente',

    sugerido_por VARCHAR(150) DEFAULT NULL,
    categoria_id INT NOT NULL,
    promocao_id INT DEFAULT NULL,
    ecossistema_id INT DEFAULT NULL,
    tipo_cultural_id INT DEFAULT NULL,

    FOREIGN KEY (sugerido_por) REFERENCES usuarios(email)
    ON DELETE SET NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    ON DELETE CASCADE,
    FOREIGN KEY (promocao_id) REFERENCES promocoes(id)
    ON DELETE SET NULL,
    FOREIGN KEY (ecossistema_id) REFERENCES ecossistemas(id)
    ON DELETE SET NULL,
    FOREIGN KEY (tipo_cultural_id) REFERENCES tipos_culturais(id)
    ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS destaques (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pontos_destaques (
    ponto_id INT NOT NULL,
    destaque_id INT NOT NULL,

    PRIMARY KEY (ponto_id, destaque_id),
    FOREIGN KEY (ponto_id) REFERENCES pontos_turisticos(id)
    ON DELETE CASCADE,
    FOREIGN KEY (destaque_id) REFERENCES destaques(id)
    ON DELETE CASCADE
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

CREATE OR REPLACE VIEW vw_pontos_turisticos AS
SELECT 
    p.id,
    p.nome,
    p.localizacao,
    p.descricao,
    p.horario_funcionamento,
    p.custo_entrada,
    p.url_imagem,
    p.categoria_id AS ponto_categoria_id,
    p.promocao_id AS ponto_promocao_id,
    p.ecossistema_id AS ponto_ecossistema_id,
    p.tipo_cultural_id AS ponto_tipo_cultural_id,
    p.area_km2,
    p.ano_fundacao,
    p.tipo_ponto,
    p.status,
    p.sugerido_por,

    c.id AS categoria_id,
    c.nome AS categoria_nome,

    pr.id AS promocao_id,
    pr.titulo AS promocao_titulo,
    pr.desconto AS promocao_desconto,
    pr.data_inicio AS promocao_data_inicio,
    pr.data_fim AS promocao_data_fim,
    pr.descricao AS promocao_descricao,

    a.ponto_id,
    a.usuario_email,
    a.nota,
    a.data_avaliacao,
    a.comentario,

    u.email,
    u.username,
    u.url_foto,
    u.tipo_usuario,

    tc.id AS tipo_cultural_id,
    tc.nome AS tipo_cultural_nome,

    e.id AS ecossistema_id,
    e.nome AS ecossistema_nome,

    d.nome AS destaque_nome,
    d.id AS destaque_id

    FROM pontos_turisticos AS p
        INNER JOIN categorias AS c ON p.categoria_id = c.id
        LEFT JOIN pontos_destaques AS pd ON pd.ponto_id = p.id
        LEFT JOIN destaques AS d ON pd.destaque_id = d.id
        LEFT JOIN ecossistemas AS e ON p.ecossistema_id = e.id
        LEFT JOIN tipos_culturais AS tc ON p.tipo_cultural_id = tc.id
        LEFT JOIN avaliacoes AS a ON a.ponto_id = p.id
        LEFT JOIN usuarios AS u ON a.usuario_email = u.email
        LEFT JOIN promocoes AS pr ON p.promocao_id = pr.id;

CREATE OR REPLACE VIEW vw_avaliacoes AS
SELECT
    a.usuario_email,
    a.ponto_id,
    a.nota,
    a.data_avaliacao,
    a.comentario,

    u.username AS usuario_username,
    u.url_foto AS usuario_url_foto,
    u.tipo_usuario,

    p.nome AS ponto_nome,
    p.localizacao AS ponto_localizacao

    FROM avaliacoes a
        INNER JOIN usuarios u ON a.usuario_email = u.email
        INNER JOIN pontos_turisticos p ON a.ponto_id = p.id;

CREATE OR REPLACE VIEW vw_usuarios_basicos AS
SELECT 
    email,
    username,
    url_foto,
    tipo_usuario,
    senha_hash
FROM usuarios;

CREATE USER 'superadmin'@'localhost'
IDENTIFIED BY 'Super@dmin'; 

CREATE USER 'admin'@'localhost'
IDENTIFIED BY '@dmin1607'; 

CREATE USER 'user'@'localhost'
IDENTIFIED BY 'Us&r123'; 

CREATE ROLE 'role_superadmin';
CREATE ROLE 'role_admin';
CREATE ROLE 'role_user';

GRANT ALL PRIVILEGES ON pontos_turisticos.* TO 'role_superadmin';

GRANT ALL PRIVILEGES ON pontos_turisticos.* TO 'role_admin';
REVOKE UPDATE, DELETE ON pontos_turisticos.usuarios FROM 'role_admin';

GRANT SELECT ON pontos_turisticos.* TO 'role_user';
GRANT INSERT, UPDATE, DELETE ON pontos_turisticos.avaliacoes TO 'role_user';
GRANT INSERT, DELETE ON pontos_turisticos.favoritos TO 'role_user';
GRANT INSERT ON pontos_turisticos.pontos_turisticos TO 'role_user';

GRANT 'role_superadmin' TO 'superadmin'@'localhost';
GRANT 'role_admin' TO 'admin'@'localhost';
GRANT 'role_user' TO 'user'@'localhost';