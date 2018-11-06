<template>
   <v-flex xs8 offset-xs2>
      <div>
       <v-flex xs8 offset-xs2>
         <span class="font-weight-light display-2">Project: {{this.project.name}}</span>
       </v-flex>
       <br />
       <v-flex xs8 offset-xs2>
         <span>
             {{this.project.startDate}} - {{this.project.endDate}}
         </span>
       </v-flex>
       <v-flex xs8 offset-xs2>
         <span>
             {{this.project.description}}
         </span>
       </v-flex>
       <br />
        <template>
          <v-tabs
            slider-color="blue"
            fixed-tabs
            v-model="mode"
            v-if="isProjectEnd"
          >
            <v-tab
              v-for="mode in ['public', 'private']"
              :key="mode"
            >
              {{ mode }}
            </v-tab>
          </v-tabs>
       </template>

       <v-card flat>
          <v-checkbox
          label="Display all entries"
          v-model="displayAll"
          ></v-checkbox>

          <v-data-table
            :headers="headers"
            :items="scores"
            :loading="loading"
            hide-actions
            class="elevation-1"
          >

            <template slot="items" slot-scope="props">
              <td>{{ props.item.rank}}</td>
              <td class="text-xs-center">
                  {{ props.item.name}}
                  <v-avatar :size=32 color="grey lighten-4" >
                      <img :src="props.item.imgURL">
                  </v-avatar>
              </td>
              <td class="text-xs-center">{{ props.item.submission_date.toLocaleString()}}</td>
              <td class="text-xs-right">{{ props.item.score}}</td>
              <td class="text-xs-right">{{ props.item.num_entries}}</td>
            </template>
          </v-data-table>
       </v-card>
     </div>
    </v-flex>
</template>

<script>
import Firebase from '../firebase';
import 'firebase/firestore';

export default {
  name: 'Index',
  data() {
    return {
      headers: [
        { text: '', value: 'rank', align: 'center' },
        {
          text: 'Name', value: 'name', sortable: false, align: 'center',
        },
        { text: 'Submission date', value: 'submission_date', align: 'center' },
        { text: 'Score', value: 'score', align: 'center' },
        { text: 'Entries', value: 'entries', align: 'center' },
      ],
      displayAll: false,
      scores: [],
      submissions: [],
      isProjectEnd: false,
      loading: true,
      mode: 0,
    };
  },
  created() {
    const today = new Date();
    this.isProjectEnd = today > new Date(this.project.endDate);
    this.getSubmissions(this.project);
  },
  computed: {
    user() {
      return this.$store.getters.user;
    },
    project() {
      return this.$store.getters.project;
    },
  },
  methods: {
    format(submissions, displayAll, mode) {
      // mode 0: public, 1: private
      const scores = [];
      const tmp = [];
      const userEntries = {};

      submissions.sort((a, b) => {
        if (mode === 0) {
          return a.public_score - b.public_score;
        }
        return a.private_score - b.private_score;
      }).forEach((submission) => {
        if (userEntries[submission.uid] === undefined) {
          userEntries[submission.uid] = 1;
        } else {
          userEntries[submission.uid] += 1;
        }
        if (!displayAll && userEntries[submission.uid] > 1) {
          // continue
          return;
        }
        tmp.push(submission);
      });

      let idx = 1;
      tmp.forEach((score) => {
        const s = {
          rank: idx,
          name: score.displayName,
          imgURL: score.imgURL,
          score: Math.round(score.public_score * 1e5) / 1e5,
          submission_date: new Date(score.submittedAt.seconds * 1000),
          num_entries: userEntries[score.uid],
        };
        if (mode === 1) {
          s.score = Math.round(score.private_score * 1e5) / 1e5;
        }
        scores.push(s);
        idx += 1;
      });

      return scores;
    },
    getSubmissions(p) {
      this.submissions = [];
      this.scores = [];
      const users = {};
      Firebase.firestore.collection('users').get().then((querySnapshot) => {
        querySnapshot.forEach((u) => {
          users[u.data().uid] = {
            displayName: u.data().displayName,
            imgURL: u.data().imgURL,
          };
        });
        Firebase.firestore.collection(`projects/${p.id}/submissions`).get().then((qs) => {
          qs.forEach((submission) => {
            const s = submission.data();
            s.displayName = users[s.uid].displayName;
            s.imgURL = users[s.uid].imgURL;
            this.submissions.push(s);
          });
          this.scores = this.format(this.submissions, this.displayAll, this.mode);
          this.loading = false;
        });
      });
    },
  },
  watch: {
    project(p) {
      if (p) {
        this.loading = true;
        const today = new Date();
        this.isProjectEnd = today > new Date(p.endDate);
        this.getSubmissions(p);
      }
    },
    displayAll(v) {
      this.scores = this.format(this.submissions, v, this.mode);
    },
    mode(v) {
      this.scores = this.format(this.submissions, this.displayAll, v);
    },
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
