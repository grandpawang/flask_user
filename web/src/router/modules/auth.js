export default [
    // 没有边框
    {
        path: '/login',
        component: resolve => require(['@/views/auth/Login.vue'], resolve)
    },
    {
        path: '/register',
        component: resolve => require(['@/views/auth/Register.vue'], resolve)
    }
]
