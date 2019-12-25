import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import i18n from './i18n'
import api from './api'
import global from '@/utils/global'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import './assets/css/icon.css';
import VueRouter from 'vue-router';

// router push catch error
const routerPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
    return routerPush.call(this, location).catch(error => error)
}

Vue.config.productionTip = false;

Vue.use(ElementUI, {
    size: 'small'
});
Vue.use(api);

Vue.prototype.$global = global;

new Vue({
    router,
    i18n,
    store,
    render: h => h(App)
}).$mount('#app');