// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import '@fortawesome/fontawesome-free/css/all.css';
import Vue from 'vue';
import Vuetify from 'vuetify';
import VeeValidate from 'vee-validate';
import UUID from 'vue-uuid';
import App from './App';
import router from './router';
import Firebase from './firebase';
import store from './store';
import 'vuetify/dist/vuetify.min.css';

Firebase.init();

Vue.use(VeeValidate);
Vue.use(UUID);
Vue.use(Vuetify, {
  iconfont: 'fa',
});
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
});
