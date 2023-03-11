# webcam-website
A flask server that displays a live webcam feed on a local network, for running on a raspberry pi

## Setup

The nginx flask server is setup with help from https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-22-04

For webcam connecting, driver support is key and some webcam drivers do not work well with systemctl (from experience). These steps should be performed inside the cloned git folder.

- Install python and update packages

```shell
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```

- Create a python virtual env

```shell
sudo apt install python3-venv
cd ~/webcam-website
python3.10 -m venv venv
source venv/bin/activate
```

- Next, install flask and uwsgi

```shell
pip install wheel
pip install uwsgi flask
pip install -r requirements.txt
nano ~/webcam-website//webcam.py
sudo ufw allow 5000
```

- At this point, you can test the app with
`uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app`

- Finally, move the system files and setup

```shell
sudo mv webcam-website.service /etc/systemd/system/webcam-website.service
sudo chgrp www-data .
sudo systemctl start webcam-website
sudo systemctl enable webcam-website
sudo systemctl status webcam-website

sudo mv webcam-website-nginx /etc/nginx/sites-available/webcam-website
sudo ln -s /etc/nginx/sites-available/webcam-website /etc/nginx/sites-enabled

sudo nginx -t
sudo systemctl restart nginx
sudo ufw delete allow 5000
sudo ufw allow 'Nginx Full'
```

- This should get an nginx flask server running on startup running the webcam.py script using the venv created.
