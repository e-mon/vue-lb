import Vue from 'vue';
import Router from 'vue-router';
import Index from '@/components/Index';
import FileUpload from '@/components/FileUpload';
import ProjectRegister from '@/components/ProjectRegister';
import MySubmission from '@/components/MySubmission';
import LeaderBoard from '@/components/LeaderBoard';
import Vuetify from 'vuetify';
import store from '../store';

Vue.use(Vuetify);
Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
      meta: { isPublic: true },
    },
    {
      path: '/lb',
      name: 'LeaderBoard',
      component: LeaderBoard,
    },
    {
      path: '/submit',
      name: 'FileUpload',
      component: FileUpload,
    },
    {
      path: '/register',
      name: 'ProjectRegister',
      component: ProjectRegister,
    },
    {
      path: '/submissions',
      name: 'MySubmission',
      component: MySubmission,
    },

  ],
});
export default router;

router.beforeEach((to, from, next) => {
  const isPublic = to.matched.some(record => record.meta.isPublic);

  if (isPublic) {
    next();
  } else if (store.getters.user.uid) {
    next();
  } else {
    next('/');
  }
});
