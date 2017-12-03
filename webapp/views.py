from flask import Flask, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort, send_from_directory
from werkzeug.utils import secure_filename
import os
import sys
import json

app = Flask(__name__)
app.config.from_object('website_config')

from webapp.models import Models, Results
from engine.engineMainFlow import run_algo
from engine.graph import DGraph

models = Models(app.config['MODELS_PATH'])
results = Results(app.config['RESULTS_PATH'])


############ main flow ##################
@app.route('/')
def model_choice_form():
    return render_template('model_choice.html', models=models.list())


@app.route('/choose_model', methods=['GET', 'POST'])
def algorithm_choice_form():
    # take model id either from form or from get param, prefer the form
    model_id = request.values.get('model_id','') or request.values.get('model', '')
    if not model_id:
        #TODO: implement flash display 
        flash('Must select valid model to choose the algorithm')
        return redirect(url_for('model_choice_form'))

    # validate the .dot file: load it
    # TODO: wrap with exception handling. Right now it's still more useful to see the exception in flask
    graph = models.open(model_id)

    errors = {}
    if request.method == 'POST':
        #TODO: validate form, run algorithm
        # params = get_params(form)
        # result = run_algo(models.open(model_id), **params)
        result = run_algo(graph, "SpectralCluster", None, stopCriteria="SizeCriteria")
        result_id = results.save(result)

        return redirect(url_for('show_results', result_id=result_id))

    #TODO: algo_data = engine.get_algorithms() instead
    algo_file_path = os.path.join(app.static_folder, 'algorithms.json')
    with open(algo_file_path) as algo_file:
        algo_data = json.load(algo_file)

    return render_template('algorithm_choice.html', model_id=model_id, errors=errors, algo_data=algo_data)


@app.route('/explore/<result_id>')
def show_results(result_id):
    # pass result id so d3 can ajax to get the json of the result
    return render_template('explorer.html', result_id=result_id)

@app.route('/results/<result_id>')
def get_result(result_id):
    "return clustering algorithm results by id"
    return jsonify(json.loads(results.open(result_id)['cluster_struct']))

def json_error(message, status_code = 400):
    "Wrap an error message in a json response. status_code is http status code"
    response = jsonify(message=message)
    response.status_code = status_code
    return response

@app.route('/models', methods=['GET', 'POST'])
def models_endpoint():
    if request.method == 'POST':
        # method == POST, handle upload
        if 'file' not in request.files:
            return json_error("TODO: missing file in post handling")
            
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if not file.filename:
            return json_error("TODO: no file in post handling")

        if not Models.allowed_filename(file.filename):
            return json_error("Bad file extension! allowed file extension: '{}'".format(EXTENSION))

        # secure filename to stop directory traversals, etc.
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['MODELS_PATH'], filename)
        if os.path.exists(path):
            return json_error("Cannot overwrite existing model")

        # write the file, finally 
        file.save(path)

        new_model = Models.filename_to_model_name(filename)
        # return list of models (now with new model)
        return jsonify(models=models.list(), new_model=new_model)
    else: # GET, return list of models

        return jsonify(models=models.list())
