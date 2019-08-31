#!/bin/bash

/etc/init.d/nginx start
sleep 2
certbot certonly --agree-tos --email vishnu.srivastava@hotmail.com --dns-google --dns-google-credentials /etc/nginx/conf.d/portfolio-251217-300d85a004e0.json -d the-software.dev -d www.the-software.dev -n
/etc/init.d/nginx stop
yes | cp -rf /etc/nginx/conf.d/default.update /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'