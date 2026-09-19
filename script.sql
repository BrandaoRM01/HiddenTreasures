-- Raul Molina Brandão | info 3 - turma 2
-- Rafael Rodrigues de Oliveira | info 3 - turma 2

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
    status ENUM('pendente', 'aprovado', 'rejeitado') NOT NULL DEFAULT 'pendente',
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

-- Tabela nova de auditoria de pontos turísticos (Questão 9)
CREATE TABLE IF NOT EXISTS log_pontos_turisticos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ponto_id INT NOT NULL,
    usuario_bd VARCHAR(150) NOT NULL,
    data_hora DATETIME NOT NULL,
    tipo_operacao ENUM('UPDATE', 'DELETE') NOT NULL,
    dados_antigos TEXT,
    dados_novos TEXT
) ENGINE=InnoDB;

-- VIEWS

-- Lista todos os pontos turísticos com informações de categoria, promoção, ecossistema, tipo cultural, avaliações e destaques
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
    a.status AS status_avaliacao,
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

-- Lista todas as avaliações com informações do usuário e do ponto turístico
CREATE OR REPLACE VIEW vw_avaliacoes AS
SELECT
    a.usuario_email,
    a.ponto_id,
    a.nota,
    a.data_avaliacao,
    a.comentario,
    a.status,

    u.username AS usuario_username,
    u.url_foto AS usuario_url_foto,
    u.tipo_usuario,

    p.nome AS ponto_nome,
    p.localizacao AS ponto_localizacao

    FROM avaliacoes a
        INNER JOIN usuarios u ON a.usuario_email = u.email
        INNER JOIN pontos_turisticos p ON a.ponto_id = p.id;

-- Lista apenas as informações básicas dos usuários
CREATE OR REPLACE VIEW vw_usuarios_basicos AS
SELECT 
    email,
    username,
    url_foto,
    tipo_usuario,
    senha_hash
FROM usuarios;

-- NOVAS (Avaliação 3 bimestre)

-- Lista dados básicos dos usuários sem expor senha, mascarando o token de recuperação
CREATE OR REPLACE VIEW vw_usuarios_seguranca AS
SELECT
    email,
    username,
    url_foto,
    tipo_usuario,
    CASE
        WHEN token_recuperacao IS NULL THEN NULL
        ELSE CONCAT(REPEAT('*', 6), RIGHT(token_recuperacao, 4))
    END AS token_recuperacao_mascarado,
    token_expiracao
FROM usuarios;

-- Relatório gerencial: pontos aprovados, nota média e favoritos por categoria
CREATE OR REPLACE VIEW vw_relatorio_categorias AS
SELECT
    c.id AS categoria_id,
    c.nome AS categoria_nome,
    COUNT(DISTINCT p.id) AS qtd_pontos_aprovados,
    ROUND(AVG(a.nota), 2) AS nota_media_categoria,
    COUNT(DISTINCT f.usuario_email, f.ponto_id) AS total_favoritos
FROM categorias AS c
    LEFT JOIN pontos_turisticos AS p
        ON p.categoria_id = c.id AND p.status = 'aprovado'
    LEFT JOIN avaliacoes AS a
        ON a.ponto_id = p.id AND a.status = 'aprovado'
    LEFT JOIN favoritos AS f
        ON f.ponto_id = p.id
GROUP BY c.id, c.nome;

-- Alerta: pontos aprovados sem avaliação ou com nota média baixa
CREATE OR REPLACE VIEW vw_pontos_risco_reputacional AS
SELECT
    p.id AS ponto_id,
    p.nome,
    p.localizacao,
    COUNT(a.usuario_email) AS qtd_avaliacoes_aprovadas,
    ROUND(AVG(a.nota), 2) AS nota_media
FROM pontos_turisticos AS p
    LEFT JOIN avaliacoes AS a
        ON a.ponto_id = p.id AND a.status = 'aprovado'
WHERE p.status = 'aprovado'
    AND (
        p.id NOT IN (SELECT ponto_id FROM avaliacoes WHERE status = 'aprovado')
        OR p.id IN (
            SELECT ponto_id FROM avaliacoes
            WHERE status = 'aprovado'
            GROUP BY ponto_id
            HAVING AVG(nota) < 3
        )
    )
GROUP BY p.id, p.nome, p.localizacao;

-- PROCEDURES

-- Aprova ou rejeita um ponto turístico sugerido
DELIMITER $$
CREATE PROCEDURE alterar_status_ponto(IN p_id INT, IN p_status VARCHAR(20))
BEGIN
    IF p_status NOT IN ('pendente', 'aprovado', 'rejeitado') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: status inválido. Use pendente, aprovado ou rejeitado.';
    END IF;

    UPDATE pontos_turisticos
    SET status = p_status
    WHERE id = p_id;
END$$
DELIMITER ;

-- Altera o tipo de um usuário (user, admin ou superadmin)
DELIMITER $$
CREATE PROCEDURE alterar_tipo_usuario(IN p_email VARCHAR(150), IN p_novo_tipo VARCHAR(20))
BEGIN
    IF p_novo_tipo NOT IN ('user', 'admin', 'superadmin') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: tipo de usuário inválido.';
    END IF;

    UPDATE usuarios
    SET tipo_usuario = p_novo_tipo
    WHERE email = p_email;
END$$
DELIMITER ;

-- Lista os pontos turísticos aprovados de uma categoria
DELIMITER $$
CREATE PROCEDURE listar_pontos_por_categoria(IN p_categoria_id INT)
BEGIN
    SELECT p.nome, p.localizacao, p.custo_entrada, c.nome AS categoria
    FROM pontos_turisticos AS p
        INNER JOIN categorias AS c ON c.id = p.categoria_id
    WHERE p.categoria_id = p_categoria_id
        AND p.status = 'aprovado';
END$$
DELIMITER ;

-- NOVAS (Avaliação 3 bimestre)

-- Efetiva o desconto vigente da promoção como novo preço-base do ponto turístico
DELIMITER $$
CREATE PROCEDURE efetivar_desconto_ponto(IN p_ponto_id INT)
BEGIN
    DECLARE v_novo_custo DECIMAL(10,2);

    SET v_novo_custo = calcular_custo_final_entrada(p_ponto_id);

    UPDATE pontos_turisticos
    SET custo_entrada = v_novo_custo,
        promocao_id = NULL
    WHERE id = p_ponto_id;
END$$
DELIMITER ;

-- Desvincula, em lote, os pontos turísticos de promoções já vencidas
DELIMITER $$
CREATE PROCEDURE processar_expiracao_promocoes()
BEGIN
    DECLARE v_fim INT DEFAULT 0;
    DECLARE v_promocao_id INT;

    DECLARE cur_promocoes CURSOR FOR
        SELECT id FROM promocoes WHERE data_fim IS NOT NULL AND data_fim < CURDATE();
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_fim = 1;

    OPEN cur_promocoes;

    loop_promocoes: LOOP
        FETCH cur_promocoes INTO v_promocao_id;
        IF v_fim = 1 THEN
            LEAVE loop_promocoes;
        END IF;

        UPDATE pontos_turisticos
        SET promocao_id = NULL
        WHERE promocao_id = v_promocao_id;
    END LOOP;

    CLOSE cur_promocoes;
END$$
DELIMITER ;

-- Valida e registra uma nova avaliação, retornando os dados consolidados
DELIMITER $$
CREATE PROCEDURE registrar_avaliacao_validada(
    IN p_usuario_email VARCHAR(150),
    IN p_ponto_id INT,
    IN p_nota INT,
    IN p_comentario TEXT
)
BEGIN
    IF usuario_pode_avaliar(p_usuario_email, p_ponto_id) = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: usuário não está elegível para avaliar este ponto turístico.';
    END IF;

    INSERT INTO avaliacoes (usuario_email, ponto_id, nota, comentario, status)
    VALUES (p_usuario_email, p_ponto_id, p_nota, p_comentario, 'pendente');

    SELECT
        p.nome AS ponto_nome,
        a.nota,
        a.status,
        a.data_avaliacao
    FROM avaliacoes AS a
        INNER JOIN pontos_turisticos AS p ON p.id = a.ponto_id
    WHERE a.usuario_email = p_usuario_email AND a.ponto_id = p_ponto_id;
END$$
DELIMITER ;

-- FUNCTIONS

-- Média das avaliações aprovadas de um ponto turístico
DELIMITER $$
CREATE FUNCTION media_avaliacoes_ponto(p_ponto_id INT)
RETURNS DECIMAL(3,2)
DETERMINISTIC
BEGIN
    RETURN (
        SELECT ROUND(AVG(nota), 2)
        FROM avaliacoes
        WHERE ponto_id = p_ponto_id
            AND status = 'aprovado'
    );
END$$
DELIMITER ;

-- Quantidade de vezes que um ponto foi favoritado
DELIMITER $$
CREATE FUNCTION qtd_favoritos_ponto(p_ponto_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN (
        SELECT COUNT(*)
        FROM favoritos
        WHERE ponto_id = p_ponto_id
    );
END$$
DELIMITER ;

-- Verifica se um ponto está com promoção ativa hoje
DELIMITER $$
CREATE FUNCTION ponto_em_promocao(p_ponto_id INT)
RETURNS TINYINT(1)
DETERMINISTIC
BEGIN
    DECLARE em_promocao TINYINT(1);

    SELECT COUNT(*) > 0 INTO em_promocao
    FROM pontos_turisticos AS p
        INNER JOIN promocoes AS pr ON pr.id = p.promocao_id
    WHERE p.id = p_ponto_id
        AND CURDATE() BETWEEN pr.data_inicio AND IFNULL(pr.data_fim, CURDATE());

    RETURN em_promocao;
END$$
DELIMITER ;

-- NOVAS (Avaliação 3 bimestre)

-- Retorna o custo de entrada de um ponto já com o desconto de promoção ativa aplicado
DELIMITER $$
CREATE FUNCTION calcular_custo_final_entrada(p_ponto_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE v_custo DECIMAL(10,2);
    DECLARE v_desconto DECIMAL(5,2);
    DECLARE v_promocao_ativa TINYINT(1);

    SELECT custo_entrada INTO v_custo
    FROM pontos_turisticos
    WHERE id = p_ponto_id;

    SET v_promocao_ativa = ponto_em_promocao(p_ponto_id);

    IF v_promocao_ativa = 1 THEN
        SELECT pr.desconto INTO v_desconto
        FROM pontos_turisticos AS p
            INNER JOIN promocoes AS pr ON pr.id = p.promocao_id
        WHERE p.id = p_ponto_id;

        RETURN ROUND(v_custo - (v_custo * v_desconto / 100), 2);
    END IF;

    RETURN v_custo;
END$$
DELIMITER ;

-- Verifica se um usuário pode avaliar um ponto (ponto aprovado e não é o próprio sugestor)
DELIMITER $$
CREATE FUNCTION usuario_pode_avaliar(p_usuario_email VARCHAR(150), p_ponto_id INT)
RETURNS TINYINT(1)
DETERMINISTIC
BEGIN
    DECLARE v_status VARCHAR(20);
    DECLARE v_sugerido_por VARCHAR(150);

    SELECT status, sugerido_por INTO v_status, v_sugerido_por
    FROM pontos_turisticos
    WHERE id = p_ponto_id;

    IF v_status IS NULL OR v_status <> 'aprovado' THEN
        RETURN 0;
    END IF;

    IF v_sugerido_por IS NOT NULL AND v_sugerido_por = p_usuario_email THEN
        RETURN 0;
    END IF;

    RETURN 1;
END$$
DELIMITER ;

-- TRIGGERS

-- Impede cadastrar ponto turístico com custo de entrada negativo
DELIMITER $$
CREATE TRIGGER before_insert_custo_entrada
BEFORE INSERT ON pontos_turisticos
FOR EACH ROW
BEGIN
    IF NEW.custo_entrada < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: custo de entrada não pode ser negativo.';
    END IF;
END$$
DELIMITER ;

-- Corrige automaticamente uma nota de avaliação fora do intervalo permitido
DELIMITER $$
CREATE TRIGGER before_update_nota_avaliacao
BEFORE UPDATE ON avaliacoes
FOR EACH ROW
BEGIN
    IF NEW.nota > 5 THEN
        SET NEW.nota = 5;
    ELSEIF NEW.nota < 1 THEN
        SET NEW.nota = 1;
    END IF;
END$$
DELIMITER ;

-- Impede favoritar um ponto turístico que ainda não foi aprovado
DELIMITER $$
CREATE TRIGGER before_insert_favorito
BEFORE INSERT ON favoritos
FOR EACH ROW
BEGIN
    IF (SELECT status FROM pontos_turisticos WHERE id = NEW.ponto_id) <> 'aprovado' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: só é possível favoritar pontos turísticos aprovados.';
    END IF;
END$$
DELIMITER ;

-- NOVAS (Avaliação 3 bimestre)

-- Grava histórico de alterações em pontos_turisticos (auditoria)
DELIMITER $$
CREATE TRIGGER after_update_pontos_log
AFTER UPDATE ON pontos_turisticos
FOR EACH ROW
BEGIN
    INSERT INTO log_pontos_turisticos (ponto_id, usuario_bd, data_hora, tipo_operacao, dados_antigos, dados_novos)
    VALUES (
        OLD.id,
        USER(),
        NOW(),
        'UPDATE',
        CONCAT('nome=', OLD.nome, '; status=', OLD.status, '; custo_entrada=', OLD.custo_entrada),
        CONCAT('nome=', NEW.nome, '; status=', NEW.status, '; custo_entrada=', NEW.custo_entrada)
    );
END$$
DELIMITER ;

-- Grava histórico de exclusões em pontos_turisticos (auditoria)
DELIMITER $$
CREATE TRIGGER after_delete_pontos_log
AFTER DELETE ON pontos_turisticos
FOR EACH ROW
BEGIN
    INSERT INTO log_pontos_turisticos (ponto_id, usuario_bd, data_hora, tipo_operacao, dados_antigos, dados_novos)
    VALUES (
        OLD.id,
        USER(),
        NOW(),
        'DELETE',
        CONCAT('nome=', OLD.nome, '; status=', OLD.status, '; custo_entrada=', OLD.custo_entrada),
        NULL
    );
END$$
DELIMITER ;

-- Impede vincular, na inserção, um ponto a uma promoção já vencida
DELIMITER $$
CREATE TRIGGER before_insert_promocao_vencida
BEFORE INSERT ON pontos_turisticos
FOR EACH ROW
BEGIN
    IF NEW.promocao_id IS NOT NULL AND EXISTS (
        SELECT 1 FROM promocoes
        WHERE id = NEW.promocao_id AND data_fim IS NOT NULL AND data_fim < CURDATE()
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: não é possível vincular o ponto a uma promoção já vencida.';
    END IF;
END$$
DELIMITER ;

-- Impede vincular, na atualização, um ponto a uma promoção já vencida
DELIMITER $$
CREATE TRIGGER before_update_promocao_vencida
BEFORE UPDATE ON pontos_turisticos
FOR EACH ROW
BEGIN
    IF NEW.promocao_id IS NOT NULL AND EXISTS (
        SELECT 1 FROM promocoes
        WHERE id = NEW.promocao_id AND data_fim IS NOT NULL AND data_fim < CURDATE()
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: não é possível vincular o ponto a uma promoção já vencida.';
    END IF;
END$$
DELIMITER ;

-- PERMISSÕES DE ACESSO DE USUÁRIOS

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