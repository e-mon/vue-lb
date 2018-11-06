<template>
   <v-flex xs8 offset-xs2>
      <div>
          <span>My submissions</span>
          <v-data-table
            :headers="headers"
            :items="submissions"
            :pagination.sync="pagination"
            hide-actions
          >
            <template slot="items" slot-scope="props">
              <td class="text-xs-center">{{ props.item.submission_date.toLocaleString()}}</td>
              <td class="text-xs-center">{{ props.item.description}}</td>
              <td class="text-xs-right">{{ props.item.score}}</td>
              <td v-if="isProjectEnd"  class="text-xs-right">
                  {{ props.item.private_score }}
              </td>
            </template>
          </v-data-table>
          <br/>
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
        { text: 'submission date', value: 'submission_date', align: 'center' },
        { text: 'Description', value: 'description', align: 'center' },
        { text: 'Score', value: 'score', align: 'center' },
        { text: 'Private Score', value: 'private_score', align: 'center' },
      ],
      pagination: {
        sortBy: 'submission_date',
        descending: true,
        rowsPerPage: -1,
      },
      loading: true,
      isProjectEnd: false,
      submissions: [],
      message: '',
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
    getSubmissions(p) {
      this.submissions = [];
      const ref = Firebase.firestore.collection(`projects/${p.id}/submissions`);
      // TODO: sort by submission date
      ref.where('uid', '==', `${this.user.uid}`).get().then((querySnapshot) => {
        querySnapshot.forEach((submission) => {
          const s = {
            score: Math.round(submission.data().public_score * 1e5) / 1e5,
            submission_date: new Date(submission.data().submittedAt.seconds * 1000),
            description: submission.data().description,
          };

          if (this.isProjectEnd) {
            s.private_score = Math.round(submission.data().private_score * 1e5) / 1e5;
          }
          this.submissions.push(s);
        });
      }).then(() => {
        this.loading = false;
      })
        .catch((error) => {
          this.message = error;
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
