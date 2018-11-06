# vue-lb

> LeaderBoard with vue.js

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

### Cloud function for evaluation

``` bash
$ cd functions && gcloud functions deploy evaluation --runtime python37 --trigger-http --project <your-project>
```

## set up credentials

### config/prod.env.js

``` js
'use strict'
module.exports = {
  NODE_ENV: '"production"',
  API_ENDPOINT: '"https://<cloud-function-url>"',
}
```

### functions/main.py
```python
# Use application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    cred, {"projectId": "<firebase-project-id>", "storageBucket": "<firebase-storage>"}
)
```

### src/firebase.js
```js
const config = {
  apiKey: '',
  authDomain: '',
  databaseURL: '',
  projectId: '',
  storageBucket: '',
  messagingSenderId: '',
};
```
