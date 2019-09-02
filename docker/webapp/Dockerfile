FROM selenium/standalone-chrome

# update debian repo
RUN apt-get update

# install and pip
RUN apt-get install python3-pip -y

WORKDIR /app

# get the req file
COPY requirements.txt /requirements.txt

# install python libraries
RUN pip3 install -r  /requirements.txt