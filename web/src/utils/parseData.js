export default {
	datetime: function (strDateTime) {
		function p(s) {
			return s < 10 ? '0' + s : s
		}
		var d = new Date(strDateTime);
		var resDate = d.getFullYear() + '-' + p((d.getMonth() + 1)) + '-' + p(d.getDate());
		var resTime = p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds());
		return resDate + ' ' + resTime
	}
}