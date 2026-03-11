## 🪟 `INSTALLATION_WINDOWS.md` (Instructions pour Windows)

```markdown
# Installation sur Windows

## 📋 Prérequis

- **Python 3.12+** : [Télécharger](https://www.python.org/downloads/)
- **PostgreSQL 15+** : [Télécharger](https://www.postgresql.org/download/windows/)
- **Git** : [Télécharger](https://git-scm.com/download/win)
- **GitHub Desktop** (optionnel) : [Télécharger](https://desktop.github.com/)
- **Memurai** (Redis pour Windows) : [Télécharger](https://www.memurai.com/get-memurai)

## 🛠️ Installation étape par étape

### 1. Vérifier Python

```powershell
python --version
pip --version

2. Installer PostgreSQL

    Lancez l'installateur PostgreSQL

    Notez le mot de passe pour l'utilisateur postgres

    Gardez le port par défaut (5432)

    Ajoutez C:\Program Files\PostgreSQL\15\bin au PATH système

3. Installer Memurai (Redis pour Windows)

    Téléchargez Memurai Developer Edition

    Lancez l'installateur

    Le service démarre automatiquement

4. Cloner le projet
powershell

# Avec GitHub Desktop
File > Clone Repository > URL: https://github.com/votre-compte/meftp_web.git

# Ou en ligne de commande
git clone https://github.com/votre-compte/meftp_web.git
cd meftp_web

5. Créer l'environnement virtuel
powershell

python -m venv venv
venv\Scripts\activate

6. Installer les dépendances
powershell

pip install --upgrade pip
pip install -r requirements.txt

7. Configurer PostgreSQL
powershell

# Ouvrir psql
psql -U postgres

sql

CREATE DATABASE meftp_web_db;
CREATE USER meftp_web_user WITH PASSWORD 'meftp_web_pw';
ALTER ROLE meftp_web_user SET client_encoding TO 'utf8';
ALTER ROLE meftp_web_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE meftp_web_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE meftp_web_db TO meftp_web_user;
\q

8. Créer le fichier d'environnement
powershell

# Créer .env à la racine du projet
notepad .env

env

SECRET_KEY=votre_clé_secrète_très_longue_et_aléatoire
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=meftp_web_db
DB_USER=meftp_web_user
DB_PASSWORD=meftp_web_pw
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0

9. Initialiser le projet
powershell

python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

10. Lancer le serveur de développement
powershell

python manage.py runserver

Accédez à http://127.0.0.1:8000/
🚀 Production avec Waitress (alternative à Gunicorn)
powershell

# Installer Waitress
pip install waitress

# Lancer le serveur
waitress-serve --port=8000 config.wsgi:application

Créer un service Windows avec NSSM

    Téléchargez NSSM

    Installez le service :

powershell

nssm install meftp "C:\chemin\vers\python.exe" "C:\chemin\vers\meftp_web\venv\Scripts\waitress-serve.exe" --port=8000 config.wsgi:application
nssm start meftp

🔧 Dépannage
Erreur psycopg2
powershell

pip uninstall psycopg2 -y
pip install psycopg2-binary

Redis ne démarre pas
powershell

# Vérifier le service Memurai
Get-Service Memurai
Start-Service Memurai

Port déjà utilisé
powershell

netstat -ano | findstr :8000
taskkill /PID [PID] /F
