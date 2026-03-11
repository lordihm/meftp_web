
## 🍏 `INSTALLATION_MAC.md` (Instructions pour macOS)

```markdown
# Installation sur macOS

## 📋 Prérequis

- **Python 3.12+**
- **Homebrew** (gestionnaire de paquets)
- **Git**
- **Xcode Command Line Tools**

## 🛠️ Installation étape par étape

### 1. Installer Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Installer Xcode Command Line Tools
bash

xcode-select --install

3. Installer les dépendances système
bash

brew update
brew install python@3.12 postgresql@15 redis nginx

4. Démarrer les services
bash

brew services start postgresql@15
brew services start redis

5. Cloner le projet
bash

git clone https://github.com/votre-compte/meftp_web.git
cd meftp_web

6. Créer l'environnement virtuel
bash

python3.12 -m venv venv
source venv/bin/activate

7. Installer les dépendances Python
bash

pip install --upgrade pip
pip install -r requirements.txt

8. Configurer PostgreSQL
bash

# Créer la base de données
psql postgres

sql

CREATE DATABASE meftp_web_db;
CREATE USER meftp_web_user WITH PASSWORD 'meftp_web_pw';
ALTER ROLE meftp_web_user SET client_encoding TO 'utf8';
ALTER ROLE meftp_web_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE meftp_web_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE meftp_web_db TO meftp_web_user;
\q

9. Créer le fichier d'environnement
bash

cat > .env << EOF
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
DB_NAME=meftp_web_db
DB_USER=meftp_web_user
DB_PASSWORD=meftp_web_pw
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
EOF

10. Initialiser le projet
bash

python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

11. Lancer le serveur de développement
bash

python manage.py runserver

