import { constantRoutes } from '@/router'
export default {
    state: { // 对数据的全局存储
        appName: '用户管理系统',  // 应用名称
        collapse: false,  // 导航栏是否收缩
        tags: [],  // 标签栏
        tagsActiveName: '',  // 当前标签页名
        menuRouteLoaded: false,    // 菜单和路由是否已经加载
        sidebar: [], // 菜单栏

    },
    mutations: { // 对数据的更改 commit
        set_collapse: (state) => { // 改变收缩状态
            // console.info("set_collapse")
            state.collapse = !state.collapse
        },
        update_tags: (state, tags) => {  // 改变tags
            // console.info("update_tags", tags)
            state.tags = tags
        },
        updateTagsActiveName: (state, name) => { // 改变当前标签页面
            // console.info("updateTagsActiveName", name)
            state.tagsActiveName = name
        },
        update_appName: (state, name) => {  //改变app名称
            // console.info("update_appName", name)
            state.appName = name;
        },
        menuRoute_loaded(state, menuRoute_loaded) {  // 菜单路由加载状态
            // console.info("menuRoute_loaded", menuRoute_loaded)
            state.menuRouteLoaded = menuRoute_loaded
        },
        update_siderbar(state, data) {
            console.log("update siderbar", data)
            state.sidebar = constantRoutes;
            data.map((val, index, arr) => {
                if (val.children && val.children.length) {
                    var count = 0;
                    val.children.map((val, index, arr) => {
                        if (val.hidden == true) { count++; }
                    })
                    if (count != val.children.length) {
                        state.sidebar = state.sidebar.concat([val])
                    }
                }
            })
            console.info("siderbar", state.sidebar)
        },
    },
    actions: {
    },
}
