FROM tiangolo/uwsgi-nginx-flask:python3.6

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
        && apt-get install -y --no-install-recommends dialog \
        && apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& apt-get install -y --no-install-recommends openssl \
    && apt install unixodbc-dev -y \
	&& echo "$SSH_PASSWD" | chpasswd

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt --no-cache-dir
ADD . /code/

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh

ENV SSL_CERT_DIR "/code/certs"
RUN chmod u+x /code/certs/generate_cert.sh
RUN ./certs/generate_cert.sh

EXPOSE 5000 2222

ENTRYPOINT ["init.sh"]