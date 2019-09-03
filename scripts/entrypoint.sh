#!/bin/bash

/etc/init.d/nginx start
sleep 2
certbot --nginx --agree-tos --email vishnu.srivastava@hotmail.com  -d 'the-software.dev,www.the-software.dev' -n
/etc/init.d/nginx stop
yes | cp -rf /etc/nginx/conf.d_new/default.conf/etc/nginx/conf.d/default.conf
/etc/init.d/nginx start
python3 app.py