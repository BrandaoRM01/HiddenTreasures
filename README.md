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

```
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
```

---

## ⚙️ Como executar

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt
flask run
```

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
