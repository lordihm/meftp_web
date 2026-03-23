🐧 INSTALLATION_LINUX.md (Instructions pour Linux)
markdown

# Installation sur Linux (Ubuntu/Debian)

## 📋 Prérequis

```bash
# Vérifier la version de Python
python3 --version  # Doit être 3.12+

# Mettre à jour les paquets
sudo apt update && sudo apt upgrade -y

🛠️ Installation étape par étape
1. Installer les dépendances système
bash

sudo apt install -y python3-pip python3-dev python3-venv \
                    postgresql postgresql-contrib libpq-dev \
                    redis-server nginx git

2. Démarrer les services
bash

sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl start redis-server
sudo systemctl enable redis-server

3. Cloner le projet
bash

git clone https://github.com/votre-compte/meftp_web.git
cd meftp_web

4. Créer l'environnement virtuel
bash

python3 -m venv venv
source venv/bin/activate

5. Installer les dépendances Python
bash

pip install --upgrade pip
pip install -r requirements.txt

6. Configurer PostgreSQL
bash

sudo -u postgres psql

sql

CREATE DATABASE meftp_web_db;
CREATE USER meftp_web_user WITH PASSWORD 'meftp_web_pw';
ALTER ROLE meftp_web_user SET client_encoding TO 'utf8';
ALTER ROLE meftp_web_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE meftp_web_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE meftp_web_db TO meftp_web_user;
\q

7. Créer le fichier d'environnement
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

8. Initialiser le projet
bash

python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

9. Configurer Gunicorn
bash

# Tester Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Créer un service systemd
sudo nano /etc/systemd/system/meftp.service

ini

[Unit]
Description=meftp gunicorn daemon
After=network.target postgresql.service redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/ubuntu/meftp_web
Environment="PATH=/home/ubuntu/meftp_web/venv/bin"
ExecStart=/home/ubuntu/meftp_web/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/ubuntu/meftp_web/meftp.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target

bash

sudo systemctl start meftp
sudo systemctl enable meftp

10. Configurer Nginx
bash

sudo nano /etc/nginx/sites-available/meftp

nginx

server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/ubuntu/meftp_web/static/;
    }
    
    location /media/ {
        alias /home/ubuntu/meftp_web/media/;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/meftp_web/meftp.sock;
    }
}

bash

sudo ln -s /etc/nginx/sites-available/meftp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

11. Configurer SSL (Let's Encrypt)
bash

sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

✅ Vérification
bash

sudo systemctl status meftp
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis

🔧 Commandes utiles
bash

# Logs
sudo journalctl -u meftp
sudo tail -f /var/log/nginx/access.log

# Redémarrer les services
sudo systemctl restart meftp
sudo systemctl reload nginx

# Mettre à jour le projet
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart meftp