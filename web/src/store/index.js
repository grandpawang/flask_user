import Vue from 'vue'
import vuex from 'vuex'

Vue.use(vuex);

import user from './modules/user'
import app from './modules/app'

const store = new vuex.Store({
    modules: {
        user: user,
        app: app,
    }
})

export default store