FROM python:3.6.10-alpine3.10 as user_server
LABEL MAINTAINER="grandpawang" description="user Manager build in flask" name="user_server"

ENV PIPURL "https://pypi.tuna.tsinghua.edu.cn/simple"
ENV PYTHONIOENCODING utf-8

WORKDIR /home/userManage/

COPY . .

RUN set -x \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk add supervisor \
    && pip --no-cache-dir install -i ${PIPURL} --upgrade pip \
    && pip --no-cache-dir install -i ${PIPURL} -r requirements

EXPOSE 8000
VOLUME /home/dev/

CMD ["/bin/sh"]
# CMD [ "gunicorn -c manage.py manage:app" ]