export default [
    {
        path: '/test',
        hidden: true,
        component: resolve => require(['@/views/tool/test.vue'], resolve)
    },
    {
        path: '/404',
        hidden: true,
        component: resolve => require(['@/views/error/404.vue'], resolve),
        meta: { title: '404' }
    },
    {
        path: '/403',
        hidden: true,
        component: resolve => require(['@/views/error/403.vue'], resolve),
        meta: { title: '403' }
    }
]
