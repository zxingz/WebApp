FROM debian:10

# update debian repo
RUN apt-get update

# install and run nginx
RUN apt-get install openssl nginx -y

# install and configure certbot (https://certbot.eff.org/lets-encrypt/debianbuster-nginx)
RUN apt install certbot python-certbot-nginx -y
#certbot --nginx --agree-tos --email vishnu.srivastava@hotmail.com -d the-software.dev -n