#!/usr/bin/env bash
#Install nginx if not istalled
sudo apt-get -y update
sudo apt-get -y install nginx

# Create folders
mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

#Create a fake file
touch /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" >> /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
myc="\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/\;\n\t}\n"
st="server {"
sudo sed -i "s/^$st/$st$myc/" /etc/nginx/sites-enabled/default
sudo service nginx start
