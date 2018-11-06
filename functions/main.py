from flask import Flask
from flask import request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from flask import jsonify
import google

import typing
from sklearn.metrics import roc_auc_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

app = Flask(__name__)

# Use application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    cred, {"projectId": "", "storageBucket": ""}
)
db = firestore.client()
bucket = storage.bucket()
metrics = {
    "auc": roc_auc_score,
    "rmse": lambda actual, pred: np.sqrt(mean_squared_error(actual, pred)),
    "mae": mean_absolute_error,
}

# for public/private split
random_state = 2018


def eval_with_metric(metric: str, actual: pd.DataFrame, pred: pd.DataFrame) -> float:
    if metric not in metrics:
        raise InvalidUsage("metric is not valid", status_code=400)

    return metrics[metric](actual, pred)


def get_datasets(
    project_id: str, submission_id: str
) -> typing.Optional[typing.Tuple[pd.DataFrame, pd.DataFrame]]:

    test_blob = bucket.blob(f"datasets/{project_id}")
    submission_blob = bucket.blob(f"submissions/{submission_id}")

    if not submission_blob.exists() or not test_blob.exists():
        print(
            "test dataset is ",
            test_blob.exists(),
            "submission is ",
            submission_blob.exists(),
        )
        return None

    test_blob.download_to_filename(f"/tmp/{project_id}.csv")
    submission_blob.download_to_filename(f"/tmp/{submission_id}.csv")

    # both datasets are apecified 0-column as index in imitation of Kaggle
    test_df = pd.read_csv(f"/tmp/{project_id}.csv", index_col=0)
    submission_df = pd.read_csv(f"/tmp/{submission_id}.csv", index_col=0)

    return submission_df, test_df


# method for validation in local
@app.route("/", methods=["POST"])
def test():
    return evaluation(request)


# default POST?
def evaluation(requests):
    print(requests.method)
    # preflight request
    if requests.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Origin, X-Requested-With, Content-Type, Accept",
        )
        return response

    # app.errorhandler is not working on cloud function...
    try:
        req = requests.get_json()
        submission_id = req.get("submission_id", "")
        project_id = req.get("project_id", "")
        if submission_id == "" or project_id == "":
            raise InvalidUsage(
                "submission_id and project_id are required", status_code=400
            )

        project_ref = db.collection("projects").document(project_id)

        print("project id:", project_id, "submission id:", submission_id)
        try:
            project = project_ref.get().to_dict()
            print(project)
            metric = project["metric"]
        except google.cloud.exceptions.NotFound:
            raise InvalidUsage("Project Not Found", status_code=400)

        ret = get_datasets(project_id, submission_id)
        if ret is None:
            raise InvalidUsage(
                "test or submission dataset is not found", status_code=400
            )
        submission_df, test_df = ret
        public_test, rest_test, public_submission, rest_submission = train_test_split(
            submission_df, test_df, test_size=0.5, random_state=random_state
        )
        public_score = eval_with_metric(metric, public_test, public_submission)
        private_score = eval_with_metric(metric, test_df, submission_df)

        response = jsonify(
            {
                "public_score": public_score,
                "private_score": private_score,
                "metric": metric,
            }
        )
    except InvalidUsage as error:
        print(error.to_dict())
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        pass
    except Exception as error:
        response = jsonify({'message' : str(error)})
        response.status_code = 500
        pass

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


# @app.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response
