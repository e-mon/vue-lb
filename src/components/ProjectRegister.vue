<template>
   <v-flex xs8 offset-xs2>
       <v-alert
         :value="alertMessage.visibility"
         :type="alertMessage.type"
       >
         {{ this.alertMessage.message }}
       </v-alert>

       <span>Project registration</span>
       <v-form ref="form">
         <v-flex xs6 sm12>
            <v-text-field
              label="Project Name"
              v-model="projectName"
              v-validate="'required'"
              data-vv-name="Project Name"
              :error-messages="errors.collect('Project Name')"
            ></v-text-field>
         </v-flex>

         <v-flex xs12>
           <v-combobox
             v-model="metric"
             :items="metrics"
             label="Metrics"
             v-validate="'required'"
             data-vv-name="Metric"
             :error-messages="errors.collect('Metric')"
           ></v-combobox>
         </v-flex>

         <v-flex xs12 sm12>
          <v-menu
            ref="startDateMenu"
            :close-on-content-click="false"
            v-model="startDateMenu"
            :nudge-right="40"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            min-width="290px"
          >
            <v-text-field
              slot="activator"
              v-model="startDate"
              label="Start Date"
              prepend-icon="event"
              readonly
              v-validate="'required'"
              data-vv-name="Start Date"
              :error-messages="errors.collect('Start Date')"
            ></v-text-field>
            <v-date-picker
              ref="picker"
              v-model="startDate"
              :min="new Date().toISOString().substr(0, 10)"
            ></v-date-picker>
          </v-menu>
         </v-flex>

         <v-flex xs12 sm12>
          <v-menu
            ref="endDateMenu"
            :close-on-content-click="false"
            v-model="endDateMenu"
            :nudge-right="40"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            min-width="290px"
          >
            <v-text-field
              slot="activator"
              v-model="endDate"
              label="End Date"
              prepend-icon="event"
              readonly
              v-validate="'required'"
              data-vv-name="End Date"
              :error-messages="errors.collect('End Date')"
            ></v-text-field>
            <v-date-picker
              ref="picker"
              v-model="endDate"
              :min="new Date().toISOString().substr(0, 10)"
            ></v-date-picker>
          </v-menu>
         </v-flex>

         <v-flex xs3 sm12>
            <v-text-field
              label="Description"
              v-model="description"
              v-validate="'required'"
              data-vv-name="Description"
              :error-messages="errors.collect('Description')"
            ></v-text-field>
         </v-flex>
         <v-flex xs12 sm12>
            <v-text-field label="Select Test Dataset"
              @click="pickFile"
              v-validate="'required'"
              data-vv-name="Test Dataset"
              :error-messages="errors.collect('Test Dataset')"
              prepend-icon='attach_file'
              v-model='fileName'>
            </v-text-field>
            <input
               type="file"
               style="display: none"
               ref="testData"
               accept=".csv"
               @change="onFilePicked"
            >
         </v-flex>
         {{this.fileName}}
         <v-progress-linear v-model="progressUpload"></v-progress-linear>
         <v-btn @click="upload" >
           submit
         </v-btn>
         <v-btn @click="clear">clear</v-btn>
       </v-form>
  </v-flex>
</template>

<script>
import firebase from 'firebase';
import { uuid } from 'vue-uuid';

export default {
  name: 'ProjectRegister',
  $_veeValidate: {
    validator: 'new',
  },
  data() {
    return {
      progressUpload: 0,
      metrics: [
        'auc',
        'rmse',
        'mae',
      ],
      metric: '',
      projectName: '',
      description: '',
      startDate: '',
      startDateMenu: false,
      endDate: '',
      endDateMenu: false,
      file: File,
      fileName: '',
      uploadTask: '',
      valid: false,
      alertMessage: { visibility: false, type: 'info', message: '' },
    };
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
    setAlert(type, message) {
      this.alertMessage = { visibility: true, type, message };
    },
    resetAlert() {
      this.alertMessage = { visibility: false, type: 'info', message: '' };
    },
    pickFile() {
      this.$refs.testData.click();
    },
    onFilePicked(e) {
      [this.file] = e.target.files;
      if (this.file !== undefined) {
        this.fileName = this.file.name;
      } else {
        this.file = '';
        this.fileName = '';
      }
    },
    upload() {
      const projectId = uuid.v4();
      this.$validator.validateAll().then((result) => {
        if (result) {
          const filepath = `datasets/${projectId}`;
          this.uploadTask = firebase.storage().ref(filepath).put(this.file);
          this.setAlert('info', 'now uploading...');
        }
      });
    },
    clear() {
      this.$refs.form.reset();
      this.file = File;
      this.fileName = '';
    },
    register(projectId) {
      const ref = firebase.firestore().collection('projects');
      ref.doc(projectId).set(
        {
          name: this.projectName,
          metric: this.metric,
          description: this.description,
          startDate: this.startDate,
          endDate: this.endDate,
          entries: 0,
        },
      ).then(() => {
        this.setAlert('success', 'project registration is finished');
      }).catch(
        (error) => {
          this.setAlert('error', error);
        },
      );
    },
  },
  watch: {
    uploadTask() {
      this.uploadTask.on('state_changed', (sp) => {
        this.progressUpload = Math.floor((sp.bytesTransferred / sp.totalBytes) * 100);
      },
      null,
      () => {
        this.uploadTask.snapshot.ref.getMetadata().then((meta) => {
          const projectId = meta.name;

          this.setAlert('info', 'registering project...');
          this.register(projectId);
        });
      });
    },
  },
};
</script>

<style>
.progress-bar {
  margin: 10px 0;
}
</style>
