
from flask import Flask, render_template, request, jsonify, flash, \
                    redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object('website_config')

import webapp.models

app.register_blueprint(webapp.models.mod)

models = webapp.models.Models(app.config['MODELS_PATH'])

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
    model = models.open(model_id)

    errors = {}
    if request.method == 'POST':
        #TODO: validate form, run algorithm
        # reqparse is a simple module for validation, matches up with argparse
        algorithm_results_id = 'placeholder'
        return redirect(url_for('show_results', result_id=algorithm_results_id))

    return render_template('algorithm_choice.html', model_id=model_id, errors=errors)


@app.route('/explore/<result_id>')
def show_results(result_id):
    # TODO: read the result and pass it back
    return render_template('explorer.html', result_id=result_id)


#TODO: un-hardcode result
import json
hardcoded_data = json.loads("""{
  "name": "root",
  "children": [
    {
     "name": "parent A",
     "children": [
       {"name": "child A1"},
       {"name": "child A2"},
       {"name": "child A3"}
     ]
    },{
     "name": "parent B",
     "children": [
       {"name": "child B1"},
       {"name": "child B2"}
     ]
    }
  ]
  }""")


@app.route('/results/<result_id>')
def get_result(result_id):
    #TODO: load actual results
    return jsonify(hardcoded_data)
