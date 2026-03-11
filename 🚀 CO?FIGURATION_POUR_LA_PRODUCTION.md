🚀 Configuration pour la production
1. Configurer Gunicorn
bash

# Créer un fichier de configuration
cat > gunicorn.conf.py << EOF
bind = "127.0.0.1:8000"
workers = 3
user = "www-data"
group = "www-data"
accesslog = "/usr/local/var/log/gunicorn-access.log"
errorlog = "/usr/local/var/log/gunicorn-error.log"
EOF

2. Configurer Nginx
bash

sudo nano /usr/local/etc/nginx/nginx.conf

nginx

http {
    # ... configuration existante ...
    
    server {
        listen 80;
        server_name votre-domaine.com;
        
        location /static/ {
            alias /Users/votre-utilisateur/meftp_web/static/;
        }
        
        location /media/ {
            alias /Users/votre-utilisateur/meftp_web/media/;
        }
        
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}

bash

sudo nginx -t
sudo brew services restart nginx

3. Créer un service launchd pour Gunicorn
bash

nano ~/Library/LaunchAgents/com.meftp.gunicorn.plist

xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.meftp.gunicorn</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/votre-utilisateur/meftp_web/venv/bin/gunicorn</string>
        <string>--config</string>
        <string>/Users/votre-utilisateur/meftp_web/gunicorn.conf.py</string>
        <string>config.wsgi:application</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/Users/votre-utilisateur/meftp_web</string>
    <key>StandardOutPath</key>
    <string>/usr/local/var/log/gunicorn-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/usr/local/var/log/gunicorn-stderr.log</string>
</dict>
</plist>

bash

launchctl load ~/Library/LaunchAgents/com.meftp.gunicorn.plist

🔧 Commandes utiles
bash

# Mettre à jour le projet
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# Redémarrer les services
brew services restart nginx
launchctl unload ~/Library/LaunchAgents/com.meftp.gunicorn.plist
launchctl load ~/Library/LaunchAgents/com.meftp.gunicorn.plist

# Voir les logs
tail -f /usr/local/var/log/gunicorn-*.log
tail -f /usr/local/var/log/nginx/access.log

✅ Vérification
bash

# Tester les services
brew services list
launchctl list | grep meftp

# Tester le site
curl http://localhost

text


## 📁 Organisation des fichiers

meftp_web/
├── README.md # Présentation du projet
├── INSTALLATION_LINUX.md # Installation sur Linux
├── INSTALLATION_WINDOWS.md # Installation sur Windows
├── INSTALLATION_MAC.md # Installation sur macOS
├── requirements.txt # Dépendances Python
└── ...