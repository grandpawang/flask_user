export default {
    array2set(arr, compare) {
        if (!compare) {
            compare = (val) => { return val }
        }
        var result = [],
            hash = {};
        for (var i = 0, elem;
            (elem = arr[i]) != null; i++) {
            if (!hash[compare(elem)]) {
                result.push(elem);
                hash[compare(elem)] = true;
            }
        }
        return result;
    }
}