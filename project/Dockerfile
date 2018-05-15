# Author: Haoji Liu
# LABEL maintainer="divid86391@hotmail.com"
FROM ubuntu:16.04

# Update OS
RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list

RUN apt-get update
RUN apt-get -y install python3-pip man build-essential python-dev curl vim net-tools ssh openssh-server supervisor sudo wget iputils-ping tree

RUN mkdir /srv/logs

ADD ./config /srv/config
RUN pip3 install --upgrade pip
RUN pip3 install -r /srv/config/requirements.txt

EXPOSE 5000 3000

# Copy config files over
ADD ./config/supervisord.conf /etc/supervisord.conf
CMD /usr/bin/supervisord -c /etc/supervisord.conf
