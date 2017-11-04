from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
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
    return "{}.{}".format(model_name, EXTENSION)

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

EXTENSION = 'dot'

def _allowed_file(filename):
    "True if filename ends with '.dot'"
    return filename.endswith('.' + EXTENSION)

@mod.route('/models', methods=['GET', 'POST'])
def models():
    if request.method == 'GET':
        return jsonify(models=list())

    # method == POST, handle upload
    if 'file' not in request.files:
        raise Exception("TODO: missing file in post handling")
        
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename:
        raise Exception("TODO: no file in post handling")

    if not file:
        raise Exception("TODO: no file case 3?!?")

    if not _allowed_file(file.filename):
        raise Exception("Allowed file extension '.{}'".format(EXTENSION))

    # secure filename to stop directory traversals, etc.
    filename = secure_filename(file.filename)
    if os.path.exists(filename):
        raise Exception("Cannot overwrite existing model")

    # write the file, finally 
    file.save(os.path.join(mod.config['MODELS_PATH'], filename))

    #TODO: return list of models anyway
    return redirect(url_for('model', model_name=filename))

@mod.route('/model/<model_name>')
def model(model_name):
    return send_from_directory(mod.config['MODELS_PATH'],
                               _model_name_to_filename(model_name))