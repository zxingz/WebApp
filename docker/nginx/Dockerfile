FROM selenium/standalone-chrome

# update debian repo
RUN sudo apt-get update

# install nginx
RUN sudo apt-get install nginx -y

# install and configure certbot (https://certbot.eff.org/lets-encrypt/debianbuster-nginx)
#RUN sudo apt-get install certbot python-certbot-nginx -y
#certbot --nginx --agree-tos --email vishnu.srivastava@hotmail.com -d the-software.dev -n

# install and pip
RUN sudo apt-get install python3-pip -y

# get the req file
COPY requirements.txt /requirements.txt

# install python libraries
RUN sudo -H pip3 install -r  /requirements.txt

WORKDIR /app