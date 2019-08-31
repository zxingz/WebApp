FROM debian:10

# update debian repo
RUN apt-get update

# install nginx
RUN apt-get install nginx -y

# install and configure certbot (https://certbot.eff.org/lets-encrypt/debianbuster-nginx)
RUN apt install certbot python-certbot-nginx -y
#certbot --nginx --agree-tos --email vishnu.srivastava@hotmail.com -d the-software.dev -n