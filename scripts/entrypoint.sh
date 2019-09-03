#!/bin/bash

sudo /etc/init.d/nginx start
sleep 2
#sudo certbot --nginx --agree-tos --email vishnu.srivastava@hotmail.com  -d 'the-software.dev,www.the-software.dev' -n
sudo etc/init.d/nginx stop
#sudo yes | cp -rf /etc/nginx/conf.d_new/default.conf /etc/nginx/conf.d/default.conf
#sudo /etc/init.d/nginx start
python3 app.py