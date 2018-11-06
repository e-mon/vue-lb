<template>
 <v-app>
    <main>
    <v-navigation-drawer
      fixed
      clipped
      app
      v-model="navBar"
    >
      <v-list>
          <v-list-tile
            v-for="item in contents"
            :key="item.title"
            :to = "item.link"
          >
            <v-list-tile-action>
               <v-icon color="black">{{item.icon}}</v-icon>
            </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title v-text="item.title"></v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-navigation-drawer>
    <v-toolbar
      dark
      color="primary"
      clipped-left
      fixed
      app
    >
      <v-toolbar-side-icon @click.stop="navBar = !navBar"></v-toolbar-side-icon>
      <v-toolbar-title class="white--text">LeaderBoard</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-combobox
        v-model="selectedProject"
        :items="projects"
        label="Select Project"
        item-text="name"
        item-value="id"
        single-line
        return-object
      ></v-combobox>
      <v-btn icon @click="reflesh">
        <v-icon>refresh</v-icon>
      </v-btn>
      <v-flex xs1  v-if="user.uid">
        <span id="userName">{{ user.displayName }}</span>
        <v-avatar
          :size=32
          color="grey lighten-4"
        >
        <img :src="user.imgURL">
        </v-avatar>
      </v-flex>
      <v-flex xs1  v-if="user.uid">
        <button type="button" @click="doLogout">
           Signout
           <v-icon>fas fa-sign-out-alt</v-icon>
        </button>
      </v-flex>
      <v-flex xs2 v-else key="logout">
        <button type="button" @click="doLogin">
           Sign in with Github
           <v-icon>fas fa-sign-in-alt</v-icon>
        </button>
      </v-flex>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height fill-width>
        <v-fade-transition mode="out-in">
          <router-view></router-view>
        </v-fade-transition>
      </v-container>
    </v-content>
    </main>
  </v-app>
</template>

<script>
import Firebase from './firebase';
import 'firebase/firestore';

export default {
  name: 'App',
  data() {
    return {
      message: '', // inform to user
      contents: [
        { title: 'Top', icon: 'fas fa-home', link: '/' },
        { title: 'LeaderBoard', icon: 'fas fa-trophy', link: '/lb' },
        { title: 'Submit', icon: 'fas fa-upload', link: '/submit' },
        { title: 'My Submittion', icon: 'fas fa-user', link: '/submissions' },
        { title: 'Project Register', icon: 'fas fa-hammer', link: '/register' },
      ],
      projects: [],
      navBar: null,
      loading: true,
    };
  },
  created() {
    Firebase.onAuth();
  },
  computed: {
    user() {
      return this.$store.getters.user;
    },
    selectedProject: {
      get() {
        return this.$store.getters.project;
      },
      set(value) {
        this.$store.commit('selectProject', value);
      },
    },
  },
  methods: {
    doLogin() {
      Firebase.login();
    },
    doLogout() {
      Firebase.logout();
    },
    reflesh() {
      this.$forceUpdate();
    },
  },
  watch: {
    user(val) {
      if (val.uid) {
        this.projects = [];
        Firebase.firestore.collection('projects').get().then((querySnapshot) => {
          this.loading = false;
          querySnapshot.forEach((project) => {
            const projectName = project.data().name;
            this.projects.push({
              name: projectName,
              docs: project.data().docs,
              description: project.data().description,
              id: project.id,
              metric: project.data().metric,
              startDate: project.data().startDate,
              endDate: project.data().endDate,
            });
          });
        });
      }
    },
  },
  destroyed() {
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
