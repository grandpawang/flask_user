import axios from '../axios'
import config from '../config'
import Cookies from "js-cookie";
/**
 * 用户管理模块
 * 
 */
export const select = (data) => {
    return axios({
        url: '/user_list',
        method: 'get',
        params: data
    })
}

export const search = (data) => {
    return axios({
        url: '/user_list',
        method: 'post',
        data: data
    })
}

export const del = (data) => {
    return axios({
        url: '/user_delete',
        method: 'get',
        params: data
    })
}

export const add_edit = (data) => {
    return axios({
        url: '/user_edit',
        method: 'post',
        data: data,
    })
}

export const upload = {
    url: config.baseUrl + "/user_upload",
    header: {
        Authorization: Cookies.get('authenticate')
    },
}