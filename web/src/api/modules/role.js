import axios from '../axios'
/**
 * 角色管理模块
 * 
 */
export const select = (data) => {
    return axios({
        url: '/role_list',
        method: 'get',
        params: data
    })
}

export const search = (data) => {
    return axios({
        url: '/role_list',
        method: 'post',
        data: data
    })
}

export const del = (data) => {
    return axios({
        url: '/role_delete',
        method: 'get',
        params: data
    })
}

export const add_edit = (data) => {
    return axios({
        url: '/role_edit',
        method: 'post',
        data: data,
    })
}