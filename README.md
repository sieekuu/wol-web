# WoL Web for Raspberry Pi

## Instalacja
sudo apt update
sudo apt install -y python3-venv python3-pip

git clone <to-repo> /home/pi/wol-web
cd /home/pi/wol-web

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# edytuj hosts.yaml (MAC już wpisane)
nano hosts.yaml

# test lokalny
export APP_SECRET=change-me
FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
# odwiedź http://IP_RPi:5000

## Autostart (systemd + gunicorn)
sudo cp wol-web.service /etc/systemd/system/wol-web.service
sudo systemctl daemon-reload
sudo systemctl enable --now wol-web.service
sudo systemctl status wol-web.service

## Opcjonalnie: reverse proxy (Nginx/HTTPS)
# standardowy układ Nginx -> Gunicorn (0.0.0.0:5000)
