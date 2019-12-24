import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import Cookies from "js-cookie"
import permission from "@/permission";
/* Layout */
import Layout from '@/Layout/index.vue'

import otherRouter from './modules/other'
import toolRouter from './modules/tool'
import authRouter from './modules/auth'
import userRouter from './modules/user'

Vue.use(Router);
const whiteList = ['/register', '/login']

export const constantRoutes = [
    ...authRouter, // system online interface
    {
        path: '/',
        redirect: '/dashboard',
        meta: {
            title: '系统首页',
            icon: "el-icon-lx-home",
            activeMenu: '/dashboard',
        },
    },
    {
        path: '/tool',
        redirect: '/',
        component: Layout,
        meta: {
            title: '工具',
            icon: "el-icon-s-tools",
            activeMenu: '/',
        },
        children: [
            ...otherRouter,
            ...toolRouter,
        ],
    },
]

export const asyncRoutes = [
    {
        path: '/userManage',
        name: "userManage",
        redirect: "/",
        // hidden: true,
        component: Layout,
        meta: {
            title: '用户管理',
            icon: "el-icon-lx-cascades",
        },
        children: userRouter,
    },
    // 404 page must be placed at the end !!!
    { path: '*', redirect: '/404' },
]



const createRouter = () => new Router({
    routes: constantRoutes,
})

const router = createRouter()


export function resetRouter() {
    const newRouter = createRouter()
    router.matcher = newRouter.matcher // reset router
}

/**
 * Filter asynchronous routing tables by recursion
 * @param asyncRouterMap asyncRoutes
 */
function filterAsyncRoutes(asyncRouterMap) {
    const res = []
    asyncRouterMap.forEach(route => {
        const tmp = { ...route }
        if (permission.has1Permissions(tmp)) {
            if (tmp.children) {
                tmp.children = filterAsyncRoutes(tmp.children)
            }
            res.push(tmp)
        }
    })
    return res
}

//使用钩子函数对路由进行权限跳转
router.beforeEach(async (to, from, next) => {
    const authenticate = Cookies.get('authenticate');
    if (authenticate) {
        if (to.path === '/login') {
            next({ path: '/' })
        }
        else {
            const hasInfo = store.state.user.info && store.state.user.permissionList.length > 0
            if (hasInfo) {
                next()
            }
            else {
                await store.dispatch('user/getInfo');  // get user info  
                await store.dispatch('user/getPermissions');  // get user permissions
                var accessedRoutes = filterAsyncRoutes(asyncRoutes);  // add async router
                store.commit("update_siderbar", accessedRoutes) // add menu

                router.addRoutes(accessedRoutes)
                console.log("accessedRoutes", accessedRoutes)
                next({ ...to, replace: true })
            }
        }
    } else {
        if (whiteList.indexOf(to.path) !== -1) {
            // in the free login whitelist, go directly
            next()
        } else {
            // other pages that do not have permission to access are redirected to the login page.
            next({ path: '/login' })
        }
    }
});

export default router