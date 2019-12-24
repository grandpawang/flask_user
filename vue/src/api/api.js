/* 
 * 接口统一集成模块
 */
import * as auth from './modules/auth'
import * as user from './modules/user'
import * as role from './modules/role'
import * as group from './modules/group'


// 默认全部导出
export default {
    auth,
    user,
    role,
    group,
}