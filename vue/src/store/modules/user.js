import api from '@/api/api'
import {resetRouter} from '@/router'
export default {
	namespaced: true,
	state: { // 对数据的全局存储
		permissionList: [],
		info: {},
	},
	mutations: { // 对数据的更改
		setPermissionList: (state, payload) => {
			var result = new Array();
			for (var key in payload) {
				var item = payload[key];
				if (item.length > 1) {
					result.push(item);
				}
			}
			state.permissionList = [].concat(...result)
		},
		setUserInfo: (state, payload) => {
			delete payload.password_hash
			// console.log(payload)
			state.info = Object.assign({}, payload)
		},
		LOGOUT: (state) => {
			state.info = {}
			state.permissionList = []
			resetRouter();
		}
	},
	actions: {
		getInfo({ commit, state }) {
			return new Promise((resolve, reject) => {
				api.auth.current_user().then((res) => {
					const data = res.data.data;
					console.log("current user", data);
					commit('setUserInfo', data);
					resolve(data)
				}).catch(error => {
					reject(error)
				})
			})
		},
		getPermissions({ commit, state }) {
			return new Promise((resolve, reject) => {
				api.auth.current_user_permission().then((res) => {
					const data = res.data.data.permissions;
					console.log("current user permission", data);
					commit('setPermissionList', data);
					resolve(data)
				}).catch(error => {
					reject(error)
				})
			})
		},
	},
}