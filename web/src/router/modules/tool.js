export default [
    {
        path: '/dashboard',
        hidden: true,
        component: resolve => require(['@/views/tool/Dashboard.vue'], resolve),
        meta: {
            icon: "el-icon-lx-home",
            title: '系统首页',
            activeMenu: "/dashboard",
        }
    },
    {
        path: '/icon',
        component: resolve => require(['@/views/tool/Icon.vue'], resolve),
        meta: {
            icon: "el-icon-lx-emoji",
            title: '自定义图标',
            activeMenu: "/icon",
        }
    },

    {
        path: '/tabs',
        component: resolve => require(['@/views/tool/Tabs.vue'], resolve),
        hidden: true,
        meta: {
            icon: "el-icon-bell",
            title: 'tab选项卡',
            activeMenu: "/tabs",
        }
    },
    {
        path: '/form',
        component: resolve => require(['@/views/tool/BaseForm.vue'], resolve),
        meta: {
            icon: "el-icon-document",
            title: '基本表单',
            activeMenu: "/form",
        }
    },
    {
        // 富文本编辑器组件
        path: '/editor',
        component: resolve => require(['@/views/tool/VueEditor.vue'], resolve),
        meta: {
            icon: "el-icon-document-add",
            title: '富文本编辑器',
            activeMenu: "/editor",
        }
    },
    {
        // markdown组件
        path: '/markdown',
        component: resolve => require(['@/views/tool/Markdown.vue'], resolve),
        meta: {
            icon: "el-icon-document-checked",
            title: 'markdown编辑器',
            activeMenu: "/markdown",
        }
    },
    {
        // vue-schart组件
        path: '/charts',
        component: resolve => require(['@/views/tool/BaseCharts.vue'], resolve),
        meta: {
            icon: "el-icon-s-data",
            title: 'schart图表',
            activeMenu: "/charts",
        }
    },
]
