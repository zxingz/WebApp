#!/bin/bash

mkdir -p /etc/letsencrypt/live/the-software.dev
openssl req -x509 -nodes -newkey rsa:1024 -days 1 -keyout '/etc/letsencrypt/live/the-software.dev/privkey.pem' -out '/etc/letsencrypt/live/the-software.dev/fullchain.pem' -subj '/CN=localhost'
nginx -g 'daemon off;'
tail -f /dev/null