<template>
  <v-flex xs8 offset-xs2>
    <v-alert
      :value="alertMessage.visibility"
      :type="alertMessage.type"
    >
      {{ this.alertMessage.message }}
    </v-alert>
    <span v-if="!project">please select project</span>
    <v-form ref="form">
      <v-flex xs12 sm12>
        <v-text-field
        v-model="projectName"
        label="Submit Project"
        v-validate="'required'"
        data-vv-name="Project Name"
        :error-messages="errors.collect('Project Name')"
        readonly
        > </v-text-field>
      </v-flex>

      <v-flex xs12 sm12>
        <v-text-field
          label="Description"
          v-model="description"
        ></v-text-field>
      </v-flex>

      <v-flex xs12 sm12>
         <v-text-field label="Select Test Dataset"
           @click="pickFile"
           v-model='fileName'
           v-validate="'required'"
           data-vv-name="Submission dataset"
           :error-messages="errors.collect('Submission dataset')"
           prepend-icon='attach_file'
           readonly
           >
         </v-text-field>
         <input
            type="file"
            style="display: none"
            ref="testData"
            accept=".csv"
            @change="onFilePicked"
         >
      </v-flex>

      <v-progress-linear v-model="progressUpload"></v-progress-linear>
      <v-btn @click="upload" >
        submit
      </v-btn>
      <v-btn @click="clear">clear</v-btn>
      <span v-if="score">{{score}}</span>
    </v-form>
  </v-flex>

</template>

<script>
import { uuid } from 'vue-uuid';
import firebase from 'firebase';
import axios from 'axios';

export default {
  name: 'FileUpload',
  data() {
    return {
      progressUpload: 0,
      description: '',
      uploadTask: '',
      file: File,
      fileName: '',
      alertMessage: { visibility: false, type: 'info', message: '' },
      score: '',
    };
  },
  mounted() {
    axios.defaults.baseURL = this.endpoint;
  },
  computed: {
    projectName() {
      return this.$store.getters.project.name;
    },
    endpoint() {
      return this.$store.getters.endpoint;
    },
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
      this.$validator.validateAll().then((result) => {
        if (result) {
          const submissionId = uuid.v4();
          const filepath = `submissions/${submissionId}`;
          this.uploadTask = firebase.storage().ref(filepath).put(this.file);

          this.setAlert('info', 'now uploading...');
        }
      });
    },
    clear() {
      this.fileName = '';
    },
    register(user, submissionId, projectId, publicScore, privateScore, description) {
      const ref = firebase.firestore().collection(`projects/${projectId}/submissions`);
      ref.doc(submissionId).set(
        {
          uid: user.uid,
          public_score: publicScore,
          private_score: privateScore,
          submission_id: submissionId,
          submittedAt: new Date(),
          description,
        },
      ).then(() => {
        const projectRef = firebase.firestore().doc(`projects/${projectId}`);
        projectRef.get().then((snapShot) => {
          console.error(snapShot.data().entries);
          projectRef.update({ entries: snapShot.data().entries + 1 });
        }).then(() => {
          this.setAlert('success', 'Finished !! Check your score in LeaderBoard');
        }).catch((error) => {
          this.setAlert('error', error.message);
        });
      }).catch(
        (error) => {
          this.setAlert('error', error.message);
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
          const submissionId = meta.name;

          this.setAlert('info', 'now scoring...');
          axios.post('evaluation', {
            submission_id: submissionId,
            project_id: this.project.id,
          }).then((response) => {
            if (response.status === 200) {
              const publicScore = response.data.public_score;
              const privateScore = response.data.private_score;
              this.register(this.user, submissionId,
                this.project.id, publicScore, privateScore, this.description);
            } else {
              console.error(response.data);
              this.setAlert('error', response.data.message);
            }
          }).catch((error) => {
            this.setAlert('error', `${error.message} - ${error.response.data.message}`);
          });
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
