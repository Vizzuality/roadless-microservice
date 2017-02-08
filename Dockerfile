FROM python:2.7-alpine
MAINTAINER Sergio Gordillo sergio.gordillo@vizzuality.com

ENV NAME flask_app
ENV USER microservice

RUN apk update && apk upgrade && \
   apk add --no-cache --update bash git openssl-dev build-base alpine-sdk \
   libffi-dev

RUN addgroup $USER && adduser -s /bin/bash -D -G $USER $USER

RUN easy_install pip && pip install --upgrade pip
RUN pip install virtualenv gunicorn gevent

RUN mkdir -p /opt/$NAME
RUN cd /opt/$NAME && virtualenv venv && source venv/bin/activate
COPY requirements.txt /opt/$NAME/requirements.txt
RUN cd /opt/$NAME && pip install -r requirements.txt

COPY main.py /opt/$NAME/main.py
COPY gunicorn.py /opt/$NAME/gunicorn.py
COPY entrypoint.sh /opt/$NAME/entrypoint.sh

# Copy the application folder inside the container
WORKDIR /opt/$NAME

RUN chown $USER:$USER /opt/$NAME
RUN chmod +x /opt/$NAME/entrypoint.sh

# Tell Docker we are going to use this port
EXPOSE 5000
# USER $USER

# Launch script
ENTRYPOINT ["./entrypoint.sh"]
#CMD [echo, "Excecuted echo in dockerfile"]