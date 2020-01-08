# vue-manage-system #

## 功能 ##
- [✔] 登录、注销、注册
- [✘] 动态路由 vue 根据权限生成的路由
- [✔] 用户管理：CRUD
- [✔] 角色管理：CRUD
- [✔] 菜单管理：CRUD
- [✔] 权限管理：CRUD
- [✔] 用户权限更改
- [✔] 加载动画


## 安装步骤 ##

``` bash
# install vue
npm install -g cnpm --registry=https://registry.npm.taobao.org 
cnpm install cnpm -g
cnpm install vue 
cnpm install --global vue-cli

# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

## 项目结构 ##

## read 
* [双向数据绑定](https://blog.csdn.net/w390058785/article/details/81076569)



## 添加动态路由
1. router.modules 添加文件
2. router.index 引入
```js
import xxx from './modules/xxx'
```
3. 在函数中添加 
    1. 一级菜单 
    2. 子菜单顺序 
    3. 权限匹配路由 
    4. 添加一级路由 菜单
```js
function filterAsyncRouter(asyncRouterMap, permissions) {
    // 一级菜单 

    let base_system_router = asyncRouterMap[0]; 

    // 子菜单顺序
    let userMenu = { // Determine display order
        user: null,
        role: null,
        group: null,
    };

    .......

    // 权限匹配路由
    for (var key in struct_permission) {
        switch (key) {
            case "user":
                base_system_router.children.push(userRouter.router.userlist)
                userMenu.user = userRouter.menu.userlist;
                break;
            case "group":
                base_system_router.children.push(userRouter.router.grouplist)
                userMenu.group = userRouter.menu.grouplist;
                break;
            case "role":
                base_system_router.children.push(userRouter.router.rolelist)
                userMenu.role = userRouter.menu.rolelist;
                break;
        }
    }

    ......

    // 添加一级路由 菜单
    router.addRoutes([base_system_router]);
    // console.info("router", router.options)
    store.commit("update_siderbar", {
        parents: "userManage",
        menu: userMenu
    });
}
```



## bug

# 第一次访问没有生成路由 第一个next()会到404

## help

* [webpack升级到4.x](https://gitee.com/xuliangzhan_admin/vue-webpack4-template/tree/master)