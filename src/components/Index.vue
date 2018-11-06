<template>
  <v-flex xs8 offset-xs2>
        <div>
            <span>Active Projects</span>
            <v-data-table
              :headers="headers"
              :items="activeProjects"
              hide-actions
              class="elevation-1"
            >
              <template slot="items" slot-scope="props">
                <td>{{ props.item.name }}</td>
                <td>{{ props.item.description}}</td>
                <td class="text-xs-right">{{ props.item.start_date }}</td>
                <td class="text-xs-right">{{ props.item.end_date}}</td>
                <td>{{ props.item.metric}}</td>
                <td class="text-xs-right">{{ props.item.entries }}</td>
              </template>
            </v-data-table>
            <br/>
            <span>Closed Projects</span>
            <v-data-table
              :headers="headers"
              :items="closedProjects"
              hide-actions
              class="elevation-1"
            >
              <template slot="items" slot-scope="props">
                <td>{{ props.item.name }}</td>
                <td>{{ props.item.description}}</td>
                <td class="text-xs-right">{{ props.item.start_date }}</td>
                <td class="text-xs-right">{{ props.item.end_date}}</td>
                <td>{{ props.item.metric}}</td>
                <td class="text-xs-right">{{ props.item.entries }}</td>
              </template>
        </v-data-table>
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
        { text: 'ProjectName', value: 'name' },
        { text: 'Description', value: 'desc' },
        { text: 'start date', value: 'start_date' },
        { text: 'end date', value: 'end_date' },
        { text: 'metric', value: 'metric' },
        { text: '#entries', value: 'entries' },
      ],
      activeProjects: [],
      closedProjects: [],
    };
  },
  computed: {
  },
  created() {
    Firebase.onAuth();
    this.closedProjects = [];
    this.activeProjects = [];

    Firebase.firestore.collection('projects').get().then((querySnapshot) => {
      this.loading = true;
      const today = new Date();

      querySnapshot.forEach((project) => {
        const p = {
          name: project.data().name,
          description: project.data().description,
          start_date: project.data().startDate,
          end_date: project.data().endDate,
          id: project.id,
          metric: project.data().metric,
          entries: project.data().entries,
        };
        if (today < new Date(project.data().endDate)) {
          this.activeProjects.push(p);
        } else {
          this.closedProjects.push(p);
        }
      });
    });
  },
  methods: {
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
