FROM nginx:1.17.3

# update debian repo
RUN apt-get update

# install and configure certbot (https://certbot.eff.org/lets-encrypt/debianbuster-nginx)
RUN apt-get install certbot python-certbot-nginx python3-certbot-dns-google -y
#certbot --nginx --agree-tos --email vishnu.srivastava@hotmail.com -d the-software.dev -n