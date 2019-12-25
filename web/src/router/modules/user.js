export default [
    {
        path: 'userlist',
        component: resolve => require(['@/views/user/User.vue'], resolve),
        meta: {
            title: '用户信息',
            activeMenu: '/userManage/userlist',
            icon: "el-icon-user-solid",
            permissions: ["user.select", "user.create", "user.delete", "user.alert"],
        }
    },
    {
        path: 'rolelist',
        component: resolve => require(['@/views/user/Role.vue'], resolve),
        meta: {
            title: '角色信息',
            activeMenu: '/userManage/rolelist',
            icon: "el-icon-s-custom",
            permissions: ["role.select", "role.create", "role.delete", "role.alert"],
        }
    },
    {
        path: 'grouplist',
        component: resolve => require(['@/views/user/Group.vue'], resolve),
        meta: {
            title: '机构信息',
            activeMenu: '/userManage/grouplist',
            icon: "el-icon-s-home",
            permissions: ["group.select", "group.create", "group.delete", "group.alert"],
        }
    },
    {
        path: '/current_user',
        hidden: true,
        component: resolve => require(['@/views/profile/index.vue'], resolve),
        meta: {
            title: '个人中心',
            activeMenu: '/current_user',
        }
    },
]