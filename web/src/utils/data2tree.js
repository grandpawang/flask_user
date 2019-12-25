export default {
    data2tree: function(data, label) {
        /**
         * data: dict
         * label: 字段翻译
         */
        var ret = [];
        for (let i in data) {
            if (Array.isArray(data[i])) {
                var res = []
                for (let j in data[i]) {
                    res.push(this.data2tree(data[i][j], label));
                }
                ret.push({
                    comment: label[i],
                    data: res,
                });
            }
        }
        if (ret.length > 0) {
            if (data.comment) {
                return {
                    comment: data.comment,
                    data: ret,
                }
            } else { // 如果是顶部的ret 则没有comment
                return ret
            }
        } else {
            return {
                comment: data.comment
            }
        }
    },
}