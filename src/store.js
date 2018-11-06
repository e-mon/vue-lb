import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: {},
    project: '',
    endpoint: process.env.API_ENDPOINT,
  },
  mutations: {
    onAuthStateChanged(state, user) {
      state.user = user;
    },
    selectProject(state, project) {
      state.project = project;
    },
  },
  getters: {
    user(state) {
      return state.user; // user()が呼ばれると、保存されたユーザー情報を返す
    },
    project(state) {
      return state.project;
    },
    endpoint(state) {
      return state.endpoint;
    },
  },
});
