export default {
    RandomStyle(alpha) {
        let r, g, b;
        r = Math.floor(Math.random() * 120) + 80;
        g = Math.floor(Math.random() * 120) + 80;
        b = Math.floor(Math.random() * 120) + 80;
        return {
            color: "rgb(" + r + ',' + g + ',' + b + ")",
            background: "rgba(" + r + ',' + g + ',' + b + ',' + alpha + ")"
        }
    }
}