from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort, send_from_directory
from flask import current_app as app
from werkzeug.utils import secure_filename
import os

from engine.graph import DGraph

mod = Blueprint('models', __name__)

def _remove_ext(filename):
    "filename.ext -> filename"
    # rfind returns -1 on not found, so we'll get the full filename
    return filename[:filename.rfind('.')]

def _filename_to_model_name(filename):
    # basename does  /path/to/file -> file
    return os.path.basename(_remove_ext(filename))

def _model_name_to_filename(model_name):
    return "{}{}".format(model_name, EXTENSION)

class Models:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def list(self):
        "Return list of model ids"
        # all valid files transformed to model ids
        model_ids = [_filename_to_model_name(filename) for filename in os.listdir(self.base_dir)
                            if _allowed_file(filename)]
        return model_ids

    def open(self, model_id):
        model_path = os.path.join(self.base_dir, _model_name_to_filename(model_id))
        return DGraph.read_dot(model_path)

EXTENSION = '.dot'

def _allowed_file(filename):
    "True if filename ends with '.dot'"
    return filename.endswith(EXTENSION)

def json_error(message, status_code = 400):
    "Wrap an error message in a json response. status_code is http status code"
    response = jsonify(message=message)
    response.status_code = status_code
    return response

@mod.route('/models', methods=['GET', 'POST'])
def models():
    if request.method == 'POST':
        # method == POST, handle upload
        if 'file' not in request.files:
            return json_error("TODO: missing file in post handling")
            
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if not file.filename:
            return json_error("TODO: no file in post handling")

        if not _allowed_file(file.filename):
            return json_error("Bad file extension! allowed file extension: '{}'".format(EXTENSION))

        # secure filename to stop directory traversals, etc.
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['MODELS_PATH'], filename)
        if os.path.exists(path):
            return json_error("Cannot overwrite existing model")

        # write the file, finally 
        file.save(path)

        new_model = _filename_to_model_name(filename)
        # return list of models (now with new model)
        return jsonify(models=Models(app.config['MODELS_PATH']).list(), new_model=new_model)
    # GET, return list of models
    return jsonify(models=Models(app.config['MODELS_PATH']).list())

@mod.route('/model/<model_name>')
def model(model_name):
    return send_from_directory(app.config['MODELS_PATH'],
                               _model_name_to_filename(model_name))
