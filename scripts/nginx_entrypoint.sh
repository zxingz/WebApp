#!/bin/bash

/etc/init.d/nginx start
sleep 2
certbot --nginx --agree-tos --email vishnu.srivastava@hotmail.com  -d 'the-software.dev,www.the-software.dev,*.the-software.dev' -n
/etc/init.d/nginx stop
yes | cp -rf /etc/nginx/conf.d/default.update /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'