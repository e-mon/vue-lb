## Installation

```bash
$ pipenv lock -r > requirements.txt
$ gcloud functions deploy evaluation --runtime python37 --trigger-http --project <project-name>
$ curl https://<region>-<project-name>.cloudfunctions.net/evaluation   -X POST -H "Content-Type: application/json" -d '{"submission_id": "boston_sample_submission", "project_id":"N08SwhQ27vi3BJ73aXaU"}'
```

## test
```bash
$ pipenv run flask
```
