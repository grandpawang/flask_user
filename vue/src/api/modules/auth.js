import axios from '../axios'

/* 
 * 系统认证模块
 */

// 登录
export const login = (data) => {
    return axios({
        url: '/login',
        method: 'post',
        data: data
    })
}

// 登出
export const logout = () => {
    return axios({
        url: 'logout',
        method: 'get'
    })
}

// 注册
export const register = (data) => {
    return axios({
        url: '/register',
        method: 'post',
        data: data
    })
}

// 获取当前用户权限信息、基本信息
export const current_user_permission = () => {
    return axios({
        url: '/current_user_permission',
        method: 'get',
    })
}

export const current_user = () => {
    return axios({
        url: '/current_user',
        method: 'get',
    })
}

