# 🌍 HiddenTreasures

Aplicação web desenvolvida com Flask para descoberta e gerenciamento de pontos turísticos, com sistema completo de usuários, avaliações e promoções.

---

## 🚀 Funcionalidades

* 👤 **Autenticação de usuários**

  * Cadastro e login
  * Controle de permissões (usuário, admin e superadmin)

* 📍 **Pontos turísticos**

  * Cadastro, edição e exclusão
  * Organização por categorias

* 🗂️ **Categorias**

  * Gerenciamento completo
  * Validação para evitar duplicidade

* ⭐ **Avaliações**

  * Comentários e avaliações dos usuários

* 💸 **Promoções**

  * Cadastro com datas de início e fim
  * Validação de desconto (0 a 100%)
  * Remoção automática de promoções expiradas
  * Separação entre promoções ativas e futuras

* 🔒 **Painel administrativo**

  * Controle total do sistema

---

## 🛠️ Tecnologias utilizadas

* **Backend:** Python + Flask
* **Banco de dados:** MySQL 
* **Frontend:** HTML, CSS, Bootstrap, Jinja2, JavaScript

---

## 📁 Estrutura do projeto

projeto/
│
├── blueprints/        # Rotas organizadas por módulos
├── dao/               # Acesso ao banco de dados
├── models/            # Modelos das entidades
├── templates/         # HTML (Jinja2)
├── static/            # CSS, imagens e arquivos estáticos
├── config/            # Configurações do sistema
├── __init__.py        # Função create_app
│
app.py                 # Inicialização da aplicação

---

## ⚙️ Como executar

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt
flask run

---

## 👥 Tipos de usuário e credenciais de teste

O sistema tem três níveis de usuário, todos herdando de uma classe base `Usuario`:

| Tipo | Como surge | `pode_moderar()` | `pode_gerenciar_usuarios()` |
|---|---|---|---|
| **User** (usuário comum) | Cadastro público em `/cadastro` | Não | Não |
| **Admin** | Promovido por um superadmin | Sim (aprova/rejeita sugestões e avaliações) | Não |
| **Superadmin** | Criado automaticamente na primeira execução, a partir do `.env` | Sim | Sim (só ele promove usuários a admin) |

**Para testar como superadmin**, use as credenciais definidas nas variáveis `SUPERADMIN_EMAIL` / `SUPERADMIN_PASSWORD` do seu `.env` (o `.env.exemplo` mostra o formato). Esse usuário é criado automaticamente por `create_app()` na primeira vez que a aplicação sobe.

**Para testar como usuário comum**, basta se cadastrar normalmente pela tela `/cadastro` com um e-mail qualquer — o cadastro público sempre cria um usuário do tipo `User`.

**Para testar como admin**, faça login como superadmin, acesse `/admin/gerenciar-usuarios` e promova o usuário comum recém-criado a `admin`.

---

## 🔑 Autenticação (JWT)

A autenticação é feita via **JWT** (`PyJWT`), sem uso de sessão no servidor:

* No login (`POST /api/usuarios/auth`), o backend confere e-mail e senha e devolve um token assinado (`SECRET_KEY`), válido por 24 horas, contendo o e-mail e o tipo do usuário.
* O front guarda o token no `localStorage` e o reenvia em todo `fetch` protegido, no cabeçalho `Authorization: Bearer <token>` (função `apiFetch` em `main.js`).
* As rotas protegidas usam os decoradores `login_required`, `admin_required` e `superadmin_required` (`decoradores.py`), que extraem e validam o token a cada requisição — nunca confiando em dados lidos do token no navegador (o menu e as permissões são sempre reconferidos via `GET /api/usuarios/me`).

**Sobre o logout:** como um JWT já emitido não pode ser invalidado no servidor sem uma lista de tokens revogados (o que não foi implementado nesta versão), a opção adotada foi **invalidar o token apenas no navegador**: o botão de logout chama `POST /logout` (que apenas confirma a ação) e, em seguida, remove o token do `localStorage`. Ou seja, o token continua tecnicamente válido até expirar (24h), mas deixa de ser enviado pelo navegador que fez logout.

---

## 🔌 API

Todas as telas (`/`, `/pontos`, `/login`, `/admin/...` etc.) são servidas pelo Flask apenas como esqueleto vazio via `render_template`, sem nenhum dado do banco. Os dados trafegam por JSON através de rotas próprias, como:

* `/api/usuarios`, `/api/usuarios/auth`, `/api/usuarios/me`, `/api/usuarios/favoritos`
* `/api/pontos`, `/api/pontos/sugestoes`, `/api/pontos/minhas-sugestoes`
* `/api/categorias`, `/api/ecossistemas`, `/api/tipos_culturais`, `/api/destaques`
* `/api/avaliacoes/ponto/<id>`

O JavaScript de cada tela busca esses dados via `fetch` e monta o HTML dinamicamente, sem recarregar a página.

---

## 🔐 Observações

* Promoções expiradas são removidas automaticamente
* Validações feitas no backend e banco de dados
* Estrutura baseada em POO + DAO

---

## 💡 Melhorias futuras

* Upload de imagens
* Recuperação de senha
* Sistema de favoritos
* API REST

---

## 👨‍💻 Autor

Desenvolvido por **Raul Molina**