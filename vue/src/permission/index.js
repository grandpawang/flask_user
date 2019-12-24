import store from '@/store'

export default {
    hasPermission: (permissions) => {
        const permissionList = store.state.user.permissionList
        if (permissionList.indexOf(permissions) === -1) {
            return false
        }
        return true
    },
    has1Permissions: (route) => {
        const permissionList = store.state.user.permissionList
        if(route.meta && route.meta.permissions){
            return permissionList.some(permission => route.meta.permissions.includes(permission))
        }else{
            return true
        }
    },
}