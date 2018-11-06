import firebase from 'firebase';
import axios from 'axios';
import store from './store';

const config = {
  apiKey: '',
  authDomain: '',
  databaseURL: '',
  projectId: '',
  storageBucket: '',
  messagingSenderId: '',
};

export default {
  init() {
    const firebaseApp = firebase.initializeApp(config);
    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION);
    this.firestore = firebaseApp.firestore();
    this.firestore.settings({ timestampsInSnapshots: true });
  },
  login() {
    const provider = new firebase.auth.GithubAuthProvider();
    firebase.auth().signInWithPopup(provider);
  },
  logout() {
    firebase.auth().signOut();
  },
  onAuth() {
    firebase.auth().onAuthStateChanged((_user) => {
      const user = _user || {};
      if (!user.uid) {
        store.commit('onAuthStateChanged', {});
      } else {
        const githubUID = user.providerData[0].uid;
        const userRef = this.firestore.collection('users').doc(`${githubUID}`);
        userRef.get().then((doc) => {
          if (doc.exists) {
            store.commit('onAuthStateChanged', doc.data());
          } else {
            axios.get(`https://api.github.com/user/${githubUID}`).then((response) => {
              const { data } = response;
              const u = {
                uid: githubUID,
                name: data.login,
                displayName: data.name || data.login,
                imgURL: data.avatar_url,
              };
              userRef.set(u).catch((err) => {
                console.error(err);
              });
              store.commit('onAuthStateChanged', u);
            }).catch((err) => {
              console.error(err);
            });
          }
        }).catch((err) => {
          console.error(err);
        });
      }
    });
  },
};
