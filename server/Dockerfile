FROM python:3.6.10-alpine3.10
LABEL MAINTAINER="grandpawang"
LABEL description="user Manager build in flask"

ENV PIPURL "https://pypi.tuna.tsinghua.edu.cn/simple"
ENV PYTHONIOENCODING utf-8

VOLUME ["/home/userManage/"]
WORKDIR /home/userManage/

COPY app ./app
COPY cache ./cache
COPY command ./command
COPY database ./database
COPY tests ./tests
COPY gunicorn.conf.py manage.py requirements ./

RUN set -x \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk add supervisor \
    && pip --no-cache-dir install -i ${PIPURL} --upgrade pip \
    && pip --no-cache-dir install -i ${PIPURL} -r requirements

EXPOSE 8000

CMD ["/bin/sh"]
