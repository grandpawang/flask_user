FROM node:lts-alpine as user_web_build
LABEL MAINTAINER="grandpawang" description="user Manager build in vue" name="user_web_build"

WORKDIR /home/userManage/

COPY . .

RUN set -x \
    && rm -rf node_modules dist \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && npm config set registry https://registry.npm.taobao.org/ \
    && npm install -g vue \
    && npm install \
    && npm run build \
    && apk add nginx
    
    # && cp dist/ /usr/share/nginx/html

EXPOSE 8080
CMD [ "/bin/sh" ]