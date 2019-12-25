import {
	baseUrl
} from '@/utils/global'

export default {
	// 基础url前缀
	baseUrl: baseUrl,
	// 请求头信息
	headers: {
		"content-type": "application/json;charset=utf-8",
	},
	// 设置超时时间
	timeout: 10000,
	// 携带凭证
	withCredentials: false,
	// 返回数据类型
	responseType: 'json'
}