-- =====================================================
-- Dados de Teste - Sistema de Gestão de Demandas
-- Município de Ceres - GO
-- =====================================================

USE Ceres_bem_cuidada;

-- Limpar dados existentes (cuidado em produção!)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE request_commentary;
TRUNCATE TABLE request_status;
TRUNCATE TABLE request_request;
TRUNCATE TABLE request_requesttype;
TRUNCATE TABLE request_statuscode;
TRUNCATE TABLE user_usuario_groups;
TRUNCATE TABLE user_usuario_user_permissions;
TRUNCATE TABLE user_usuario;
TRUNCATE TABLE user_usertype;
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- 1. TIPOS DE USUÁRIO
-- =====================================================
INSERT INTO user_usertype (id, `desc`) VALUES
(1, 'Cidadão'),
(2, 'Gestor da Prefeitura'),
(3, 'Administrador');

-- =====================================================
-- 2. CÓDIGOS DE STATUS
-- =====================================================
INSERT INTO request_statuscode (id, `desc`) VALUES
(1, 'Em análise'),
(2, 'Em andamento'),
(3, 'Aguardando material'),
(4, 'Concluída'),
(5, 'Cancelada');

-- =====================================================
-- 3. TIPOS DE SOLICITAÇÃO
-- =====================================================
INSERT INTO request_requesttype (id, icon, banner, `desc`, title) VALUES
(1, 'assets/icon_buraco.png', 'assets/banner_buraco.png', 'Buraco na via pública', 'Pavimentação'),
(2, 'assets/icon_arvore.png', 'assets/banner_arvore.png', 'Árvore caída ou galhos perigosos', 'Poda de árvore'),
(3, 'assets/icon_iluminacao.png', 'assets/banner_iluminacao.png', 'Poste queimado ou sem iluminação', 'Iluminação pública'),
(4, 'assets/icon_calcada.png', 'assets/banner_calcada.png', 'Calçada quebrada ou irregular', 'Calçada'),
(5, 'assets/icon_lixo.png', 'assets/banner_lixo.png', 'Lixo acumulado ou entulho', 'Coleta de lixo'),
(6, 'assets/icon_saneamento.png', 'assets/banner_saneamento.png', 'Esgoto entupido ou vazamento', 'Saneamento'),
(7, 'assets/icon_sinalizacao.png', 'assets/banner_sinalizacao.png', 'Placa danificada ou ausente', 'Sinalização');

-- =====================================================
-- 4. USUÁRIOS
-- =====================================================
-- Senha para todos: "senha123" (hash bcrypt)
-- pbkdf2_sha256$600000$saltvalue... (Django hash)

-- Cidadãos
INSERT INTO user_usuario (
    id, password, last_login, is_superuser, first_name, last_name, nome, dataNasc, cpf, endereco, 
    telefone, email, userType_id, is_staff, is_active, date_joined
) VALUES
(1, 'pbkdf2_sha256$600000$salt1$hash1', NULL, 0, '', '', 'João da Silva', '1985-03-15', '123.456.789-01', 
 'Rua das Flores, 123, Centro, Ceres-GO', '62999887766', 'joao.silva@email.com', 1, 0, 1, NOW()),
 
(2, 'pbkdf2_sha256$600000$salt2$hash2', NULL, 0, '', '', 'Maria Santos', '1990-07-22', '234.567.890-12', 
 'Av. Brasil, 456, São João, Ceres-GO', '62988776655', 'maria.santos@email.com', 1, 0, 1, NOW()),
 
(3, 'pbkdf2_sha256$600000$salt3$hash3', NULL, 0, '', '', 'Pedro Oliveira', '1978-11-30', '345.678.901-23', 
 'Rua Goiás, 789, Centro, Ceres-GO', '62977665544', 'pedro.oliveira@email.com', 1, 0, 1, NOW()),
 
(4, 'pbkdf2_sha256$600000$salt4$hash4', NULL, 0, '', '', 'Ana Costa', '1995-02-14', '456.789.012-34', 
 'Rua Tocantins, 321, Vila Nova, Ceres-GO', '62966554433', 'ana.costa@email.com', 1, 0, 1, NOW()),
 
(5, 'pbkdf2_sha256$600000$salt5$hash5', NULL, 0, '', '', 'Carlos Mendes', '1988-09-05', '567.890.123-45', 
 'Av. Central, 654, Centro, Ceres-GO', '62955443322', 'carlos.mendes@email.com', 1, 0, 1, NOW());

-- Gestores
INSERT INTO user_usuario (
    id, password, last_login, is_superuser, first_name, last_name, nome, dataNasc, cpf, endereco, 
    telefone, email, userType_id, is_staff, is_active, date_joined
) VALUES
(6, 'pbkdf2_sha256$600000$salt6$hash6', NULL, 0, '', '', 'Roberto Gestor', '1975-05-20', '678.901.234-56', 
 'Rua Prefeitura, 100, Centro, Ceres-GO', '62944332211', 'roberto.gestor@prefeitura.ceres.go.gov.br', 2, 1, 1, NOW()),
 
(7, 'pbkdf2_sha256$600000$salt7$hash7', NULL, 0, '', '', 'Juliana Administradora', '1982-08-12', '789.012.345-67', 
 'Av. Prefeitura, 200, Centro, Ceres-GO', '62933221100', 'juliana.admin@prefeitura.ceres.go.gov.br', 2, 1, 1, NOW());

-- Administrador
INSERT INTO user_usuario (
    id, password, last_login, is_superuser, first_name, last_name, nome, dataNasc, cpf, endereco, 
    telefone, email, userType_id, is_staff, is_active, date_joined
) VALUES
(8, 'pbkdf2_sha256$600000$salt8$hash8', NULL, 1, '', '', 'Admin Sistema', '1980-01-01', '890.123.456-78', 
 'Prefeitura Municipal, Centro, Ceres-GO', '62922110099', 'admin@prefeitura.ceres.go.gov.br', 3, 1, 1, NOW());

-- =====================================================
-- 5. SOLICITAÇÕES
-- =====================================================

-- Solicitação 1: Buraco na via - Concluída
INSERT INTO request_request (
    id, id_user_id, request_type_id, importance, img1, img2, img3, 
    `comment`, lat, lon, created, completed, is_canceled, 
    current_status_id, current_status_updated_at
) VALUES
(1, 1, 1, NULL, 'fotos/20/02/2026/abc123.jpg', 'fotos/20/02/2026/def456.jpg', 'fotos/20/02/2026/ghi789.jpg',
 'Buraco grande na Rua das Flores altura do número 500. Está causando risco de acidentes para motociclistas.',
 '-15.3145', '-49.5980', '2026-02-20 08:30:00', '2026-02-24 16:00:00', 0, 4, '2026-02-24 16:00:00');

-- Solicitação 2: Iluminação - Em andamento
INSERT INTO request_request (
    id, id_user_id, request_type_id, importance, img1, img2, img3, 
    `comment`, lat, lon, created, completed, is_canceled, 
    current_status_id, current_status_updated_at
) VALUES
(2, 2, 3, NULL, 'fotos/21/02/2026/jkl012.jpg', 'fotos/21/02/2026/mno345.jpg', 'fotos/21/02/2026/pqr678.jpg',
 'Poste de iluminação queimado na esquina da Av. Brasil com Rua Goiás. Local está escuro à noite.',
 '-15.3150', '-49.5975', '2026-02-21 14:20:00', NULL, 0, 2, '2026-02-23 10:30:00');

-- Solicitação 3: Lixo acumulado - Em análise
INSERT INTO request_request (
    id, id_user_id, request_type_id, importance, img1, img2, img3, 
    `comment`, lat, lon, created, completed, is_canceled, 
    current_status_id, current_status_updated_at
) VALUES
(3, 3, 5, NULL, 'fotos/22/02/2026/stu901.jpg', 'fotos/22/02/2026/vwx234.jpg', 'fotos/22/02/2026/yza567.jpg',
 'Acúmulo de lixo na Praça Central. O lixo não está sendo coletado há mais de uma semana.',
 '-15.3155', '-49.5985', '2026-02-22 09:15:00', NULL, 0, 1, '2026-02-22 09:15:00');

-- Solicitação 4: Árvore caída - Aguardando material
INSERT INTO request_request (
    id, id_user_id, request_type_id, importance, img1, img2, img3, 
    `comment`, lat, lon, created, completed, is_canceled, 
    current_status_id, current_status_updated_at
) VALUES
(4, 4, 2, NULL, 'fotos/23/02/2026/bcd890.jpg', 'fotos/23/02/2026/efg123.jpg', 'fotos/23/02/2026/hij456.jpg',
 'Árvore com galhos perigosos na Rua Tocantins. Pode cair sobre veículos e pedestres.',
 '-15.3140', '-49.5990', '2026-02-23 11:45:00', NULL, 0, 3, '2026-02-24 14:20:00');

-- Solicitação 5: Calçada quebrada - Em andamento
INSERT INTO request_request (
    id, id_user_id, request_type_id, importance, img1, img2, img3, 
    `comment`, lat, lon, created, completed, is_canceled, 
    current_status_id, current_status_updated_at
) VALUES
(5, 5, 4, NULL, 'fotos/23/02/2026/klm789.jpg', 'fotos/23/02/2026/nop012.jpg', 'fotos/23/02/2026/qrs345.jpg',
 'Calçada completamente quebrada na Av. Central. Dificulta passagem de pedestres e cadeirantes.',
 '-15.3148', '-49.5978', '2026-02-23 15:30:00', NULL, 0, 2, '2026-02-24 10:00:00');

-- Solicitação 6: Saneamento - Em análise
INSERT INTO request_request (
    id, id_user_id, request_type_id, importance, img1, img2, img3, 
    `comment`, lat, lon, created, completed, is_canceled, 
    current_status_id, current_status_updated_at
) VALUES
(6, 1, 6, NULL, 'fotos/24/02/2026/tuv678.jpg', 'fotos/24/02/2026/wxy901.jpg', 'fotos/24/02/2026/zab234.jpg',
 'Esgoto entupido na Rua das Flores. Mau cheiro está insuportável.',
 '-15.3142', '-49.5982', '2026-02-24 07:50:00', NULL, 0, 1, '2026-02-24 07:50:00');

-- Solicitação 7: Sinalização - Concluída
INSERT INTO request_request (
    id, id_user_id, request_type_id, importance, img1, img2, img3, 
    `comment`, lat, lon, created, completed, is_canceled, 
    current_status_id, current_status_updated_at
) VALUES
(7, 2, 7, NULL, 'fotos/18/02/2026/cde567.jpg', 'fotos/18/02/2026/fgh890.jpg', 'fotos/18/02/2026/ijk123.jpg',
 'Placa de PARE ausente no cruzamento. Risco de acidentes.',
 '-15.3152', '-49.5988', '2026-02-18 13:20:00', '2026-02-22 11:30:00', 0, 4, '2026-02-22 11:30:00');

-- Solicitação 8: Buraco - Cancelada (duplicada)
INSERT INTO request_request (
    id, id_user_id, request_type_id, importance, img1, img2, img3, 
    `comment`, lat, lon, created, completed, is_canceled, 
    current_status_id, current_status_updated_at
) VALUES
(8, 3, 1, NULL, 'fotos/19/02/2026/lmn456.jpg', 'fotos/19/02/2026/opq789.jpg', 'fotos/19/02/2026/rst012.jpg',
 'Buraco na via - mesma localização da solicitação anterior.',
 '-15.3145', '-49.5980', '2026-02-19 16:40:00', NULL, 1, 5, '2026-02-19 17:00:00');

-- =====================================================
-- 6. HISTÓRICO DE STATUS
-- =====================================================

-- Histórico Solicitação 1 (Buraco - Concluída)
INSERT INTO request_status (id, id_request_id, status_code_id, dateTime) VALUES
(1, 1, 1, '2026-02-20 08:30:00'),  -- Em análise
(2, 1, 2, '2026-02-21 10:15:00'),  -- Em andamento
(3, 1, 4, '2026-02-24 16:00:00');  -- Concluída

-- Histórico Solicitação 2 (Iluminação - Em andamento)
INSERT INTO request_status (id, id_request_id, status_code_id, dateTime) VALUES
(4, 2, 1, '2026-02-21 14:20:00'),  -- Em análise
(5, 2, 2, '2026-02-23 10:30:00');  -- Em andamento

-- Histórico Solicitação 3 (Lixo - Em análise)
INSERT INTO request_status (id, id_request_id, status_code_id, dateTime) VALUES
(6, 3, 1, '2026-02-22 09:15:00');  -- Em análise

-- Histórico Solicitação 4 (Árvore - Aguardando material)
INSERT INTO request_status (id, id_request_id, status_code_id, dateTime) VALUES
(7, 4, 1, '2026-02-23 11:45:00'),  -- Em análise
(8, 4, 2, '2026-02-24 09:00:00'),  -- Em andamento
(9, 4, 3, '2026-02-24 14:20:00');  -- Aguardando material

-- Histórico Solicitação 5 (Calçada - Em andamento)
INSERT INTO request_status (id, id_request_id, status_code_id, dateTime) VALUES
(10, 5, 1, '2026-02-23 15:30:00'), -- Em análise
(11, 5, 2, '2026-02-24 10:00:00'); -- Em andamento

-- Histórico Solicitação 6 (Saneamento - Em análise)
INSERT INTO request_status (id, id_request_id, status_code_id, dateTime) VALUES
(12, 6, 1, '2026-02-24 07:50:00'); -- Em análise

-- Histórico Solicitação 7 (Sinalização - Concluída)
INSERT INTO request_status (id, id_request_id, status_code_id, dateTime) VALUES
(13, 7, 1, '2026-02-18 13:20:00'), -- Em análise
(14, 7, 2, '2026-02-19 08:00:00'), -- Em andamento
(15, 7, 4, '2026-02-22 11:30:00'); -- Concluída

-- Histórico Solicitação 8 (Cancelada)
INSERT INTO request_status (id, id_request_id, status_code_id, dateTime) VALUES
(16, 8, 1, '2026-02-19 16:40:00'), -- Em análise
(17, 8, 5, '2026-02-19 17:00:00'); -- Cancelada

-- =====================================================
-- 7. COMENTÁRIOS
-- =====================================================

-- Comentários na Solicitação 1 (Buraco - Concluída)
INSERT INTO request_commentary (id, id_request_id, id_user_id, message, created_at) VALUES
(1, 1, 6, 'Equipe de pavimentação foi acionada. Prazo estimado: 3 dias úteis.', '2026-02-21 11:00:00'),
(2, 1, 1, 'Obrigado pelo retorno!', '2026-02-21 14:30:00'),
(3, 1, 6, 'Serviço concluído. Obrigado pela solicitação.', '2026-02-24 16:15:00');

-- Comentários na Solicitação 2 (Iluminação - Em andamento)
INSERT INTO request_commentary (id, id_request_id, id_user_id, message, created_at) VALUES
(4, 2, 7, 'Solicitação encaminhada para a equipe de manutenção elétrica.', '2026-02-22 09:00:00'),
(5, 2, 6, 'Material para reparo já separado. Equipe iniciará amanhã.', '2026-02-23 10:45:00'),
(6, 2, 2, 'Aguardando ansiosamente o reparo. Obrigada!', '2026-02-23 15:20:00');

-- Comentários na Solicitação 4 (Árvore - Aguardando material)
INSERT INTO request_commentary (id, id_request_id, id_user_id, message, created_at) VALUES
(7, 4, 6, 'Equipe vistoriou o local. Necessário equipamento especial para poda.', '2026-02-24 10:30:00'),
(8, 4, 4, 'Entendo. Quando terá o equipamento disponível?', '2026-02-24 12:00:00'),
(9, 4, 6, 'Equipamento chegará na próxima semana. Trabalho será priorizado.', '2026-02-24 14:30:00');

-- Comentários na Solicitação 5 (Calçada - Em andamento)
INSERT INTO request_commentary (id, id_request_id, id_user_id, message, created_at) VALUES
(10, 5, 7, 'Obra de recuperação da calçada foi incluída no cronograma desta semana.', '2026-02-24 11:00:00');

-- Comentários na Solicitação 7 (Sinalização - Concluída)
INSERT INTO request_commentary (id, id_request_id, id_user_id, message, created_at) VALUES
(11, 7, 6, 'Placa de PARE instalada conforme solicitado.', '2026-02-22 11:45:00'),
(12, 7, 2, 'Perfeito! Já está instalada. Muito obrigada!', '2026-02-22 14:00:00');

-- Comentários na Solicitação 8 (Cancelada)
INSERT INTO request_commentary (id, id_request_id, id_user_id, message, created_at) VALUES
(13, 8, 6, 'Esta solicitação é duplicada. Já existe registro anterior para o mesmo local.', '2026-02-19 17:05:00');

-- =====================================================
-- Resetar AUTO_INCREMENT para próximos registros
-- =====================================================
ALTER TABLE user_usertype AUTO_INCREMENT = 4;
ALTER TABLE user_usuario AUTO_INCREMENT = 9;
ALTER TABLE request_statuscode AUTO_INCREMENT = 6;
ALTER TABLE request_requesttype AUTO_INCREMENT = 8;
ALTER TABLE request_request AUTO_INCREMENT = 9;
ALTER TABLE request_status AUTO_INCREMENT = 18;
ALTER TABLE request_commentary AUTO_INCREMENT = 14;

-- =====================================================
-- FIM
-- =====================================================
SELECT 'Dados de teste inseridos com sucesso!' as Status;
