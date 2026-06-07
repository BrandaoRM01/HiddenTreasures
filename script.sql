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
    status ENUM('pendente', 'aprovado', 'rejeitado') NOT NULL DEFAULT 'pendente',

    categoria_id INT NOT NULL,
    promocao_id INT DEFAULT NULL,
    ecossistema_id INT DEFAULT NULL,
    tipo_cultural_id INT DEFAULT NULL,

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

INSERT INTO categorias (id, nome, descricao) VALUES
(11, 'Praia', 'Mar e areia'),
(12, 'Montanha', 'Lugar belo e alto'),
(13, 'Monumento', 'Algo feito pelo homem e que marcou a história'),
(14, 'Museu', 'Lugar onde se admirar obras de arte'),
(15, 'Cidade histórica', 'Cidade marcada por importância histórica'),
(16, 'Cânion', 'Grande buraco natural'),
(19, 'Local histórico', 'Sem descrição'),
(20, 'Parque ecológico', 'Sem descrição'),
(21, 'Edifício', 'Sem descrição'),
(22, 'Torre', 'Sem descrição'),
(23, 'Shopping', 'Sem descrição'),
(24, 'Floresta', 'Sem descrição');

INSERT INTO promocoes 
(id, titulo, descricao, desconto, data_inicio, data_fim)
VALUES
(3, 'Promoção de natal - 2026', 
'Promoção perfeita para seu fim de ano', 
45.50, '2026-12-01', '2026-12-30'),

(4, 'Promoção internacional', 
'Promoção para pessoas que pretendem visitar lugares distantes pelo mundo!', 
35.00, '2026-04-03', '2026-05-15');

INSERT INTO pontos_turisticos 
(id, nome, localizacao, descricao, horario_funcionamento, custo_entrada, url_imagem, categoria_id, promocao_id)
VALUES
(18, 'Grand canyon', 'Arizona, EUA', 'Conhecido pelas suas camadas rochosas vermelhas que revelam bilhões de anos da história da terra, é um patrimônio mundial da UNESCO e um dos parques nacionais mais visitados', '24 horas por dia', 120.00, 'uploads/pontos/grand_canyon.jpg', 16, 4),

(20, 'Muralha da China', 'China', 'A grande muralha da china é uma série de fortificações na china, construída ao longo das fronteiras históricas para proteção', '7:30 às 18:30', 390.00, 'uploads/pontos/muralha_da_china.jpg', 19, NULL),

(21, 'Parque Natural Municipal do Basalto', 'Araraquara, SP, Brasil', 'Parque ecológico em Araraquara', '08 às 18', 0.00, 'uploads/pontos/parque_natural_municipal_do_basalto.jpg', 20, NULL),

(22, 'Ouro Preto', 'Minas Gerais, Brasil', 'Uma cidade histórica famosa do Brasil', 'Dia todo', 0.00, 'uploads/pontos/ouro_preto.jpg', 15, NULL),

(23, 'Torre Eiffel', 'Paris, França', 'Uma torre muito linda e alta', 'Dia todo', 100.00, 'uploads/pontos/torre_eiffel.jpg', 13, 4),

(24, 'Coliseu', 'Roma, Itália', 'Um antigo edifício famoso na época da política do pão e circo', '10 às 18', 100.00, 'uploads/pontos/coliseu.jpg', 19, 4),

(25, 'Cristo Redentor', 'Rio de Janeiro, Brasil', 'Um monumento famoso considerado uma das sete maravilhas do mundo', 'Dia todo', 25.00, 'uploads/pontos/cristo_redentor.webp', 13, NULL),

(27, 'Shopping Jaraguá', 'Araraquara, SP, Brasil', 'Shopping center em Araraquara', '08 às 22 horas', 0.00, 'uploads/pontos/shopping_jaragua.jpg', 23, NULL),

(28, 'Bueno de Andrada', 'Bueno de Andrada, SP, Brasil', 'Cidade conhecida pelas coxinhas', 'Dia todo', 0.00, 'uploads/pontos/bueno_de_andrada.jpg', 15, NULL),

(29, 'Douradinhas de Nova Pauliceia', 'Nova Pauliceia, SP, Brasil', 'Lugar maravilhoso', 'Dia todo', 0.00, 'img/default/hidden_treasures_logo.png', 15, NULL),

(30, 'Cristo de Araraquara', 'Araraquara, SP, Brasil (Melhado, rodoviária)', 'Ponto de entretenimento e diversão', '18h às 6h', 300.00, 'uploads/pontos/cristo_de_araraquara.jpg', 13, NULL),

(31, 'Caesars Palace', 'Las Vegas, EUA', 'Resort e cassino icônico inspirado na Roma antiga', '24h', 0.00, 'uploads/pontos/caesars_palace.jpg', 21, NULL),

(32, 'Vila Belmiro', 'Santos, SP, Brasil', 'Estádio histórico do Santos FC com grande importância esportiva', '08:00 às 24:00', 150.00, 'uploads/pontos/villa_belmiro.jpg', 19, NULL);