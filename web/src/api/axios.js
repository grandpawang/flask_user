import Axios from 'axios'
import router from '@/router'
import config from './config';
import Cookies from "js-cookie";
// http request 拦截器
export default function $axios(options) {
    return new Promise((resolve, reject) => {
        var instance = Axios.create({
            baseURL: config.baseUrl,
            headers: config.headers,
            timeout: config.timeout,
            withCredentials: config.withCredentials,
        });
        instance.interceptors.request.use(
            conf => {
                var authenticate = Cookies.get('authenticate');
                if (authenticate != "") { // 判断是否存在token，如果存在的话，则每个http header都加上token
                    conf.headers.Authorization = authenticate;
                }
                return conf;
            },
            err => {
                return Promise.reject(err);
            }
        );
        // http response 拦截器 authenticate过期跳转登录
        instance.interceptors.response.use(
            response => {
                return response;
            },
            error => {
                if (error.response) {
                    // console.log(error);
                    // console.log('axios:' + error.response.status);
                    switch (error.response.status) {
                        case 401:
                            router.replace({
                                path: 'login',
                                query: {
                                    redirect: router.currentRoute.fullPath
                                }
                            });
                    }
                }
                return Promise.reject(error); // 返回接口返回的错误信息
            }
        );
        // 请求处理
        instance(options).then(res => {
            resolve(res)
        }).catch(error => {
            reject(error)
        });
    })
}