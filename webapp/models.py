from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
import os

mod = Blueprint('models', __name__)

def _remove_ext(filename):
    "filename.ext -> filename"
    # rfind returns -1 on not found, so we'll get the full filename
    return filename[filename.rfind('.') + 1:]

def _filename_to_model_name(filename):
    # basename does  /path/to/file -> file
    return os.path.basename(_remove_ext(filename))

def _model_name_to_filename(model_name):
    return "{}.{}".format(model_name, EXTENSION)

class Models:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def list(self):
        return [_filename_to_model_name(filename) for filename in os.listdir(self.base_dir)]


EXTENSION = 'dot'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1]==EXTENSION

@mod.route('/models', methods=['GET', 'POST'])
def models():
    if request.method == 'GET':
        return jsonify(models=Models.list())

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

    if not allowed_file(file.filename):
        raise Exception("Allowed file extension '.{}'".format(EXTENSION))

    # secure filename to stop directory traversals, etc.
    filename = secure_filename(file.filename)

    # write the file, finally 
    file.save(os.path.join(mod.config['MODELS_PATH'], filename))

    #TODO: return list of models anyway
    return redirect(url_for('model', model_name=filename))

@mod.route('/model/<model_name>')
def model(model_name):
    return send_from_directory(mod.config['MODELS_PATH'],
                               _model_name_to_filename(model_name))