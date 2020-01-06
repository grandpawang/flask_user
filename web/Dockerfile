FROM node:8.17-alpine
LABEL MAINTAINER="grandpawang"
LABEL description="user Manager build in vue"

WORKDIR /home/userManage/

COPY build build/
COPY config config/
COPY src src/
COPY static static/
COPY test test/
COPY build build/
COPY .babelrc .editorconfig .postcssrc.js index.html package.json ./

RUN set -x \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && npm config set registry https://registry.npm.taobao.org/ \
    && npm install -g vue \
    && npm install -g vue-router \
    && npm install \
    # && npm run build \
    && ls

EXPOSE 8080
VOLUME /home/userManage/

CMD [ "/bin/sh" ]