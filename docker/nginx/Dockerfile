FROM nginx:1.17.3

# update debian repo
RUN apt-get update

# install and configure certbot (https://certbot.eff.org/lets-encrypt/debianbuster-nginx)
RUN apt install certbot python-certbot-nginx -y
#certbot --nginx --agree-tos --email vishnu.srivastava@hotmail.com -d the-software.dev -n