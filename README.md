# README #

This repo contains model_exploration, a web-app to facilitate exploring software models represented as directed graphs (e.g. state machines), using hierarchical clustering with user input to choose the level of abstraction displayed,

### Table of Contents

**[How do I get set up?](#setup)**<br>
**[Configuration](#configuration)**<br>
**[Running](#configuration)**<br>

### Setup

* Dependencies

pydot implicitly requires python 3 <-> Tk integration. In Ubuntu/Debian, run:

`sudo apt install python3-tk`

Working git with ssh is required.

* Setup

Check out the git repository.

(optional) Set up a virtualenv: in linux run `virtualenv venv` and then `source ./venv/bin/activate`, in windows run `virtualenv venv` and then `.\venv\bin\activate.bat`

Install dependencies by running `pip3 install -r requirements.txt`

*NOTE:* Working git with ssh is required. GEM (Graph Embedding Methods) is installed from github directly since PyPI contains an outdated version at the moment (v0.1.12 at writing).

At this point, running `py.test` from project root should successfully pass all tests

### Configuration

`webapp_config.py` contains configuration for the web application:

* MODELS_PATH [<project dir>/models_dot/] - path to directory containing the .dot files representing models
* RESULTS_PATH [<project dir>/results/] - path to directory that will contain results of runs
* LOGGING_CONFIG [<project dir>/logging.conf (YAML)] - standard python logging configuration (log rotation, format, etc.). default stores logs in <project dir>/logs/
Flask


### Running

* How to run tests

To run all tests run the following command from the main project folder: `py.test`

* How to run the server

`python3 run_webapp.py` will run the server

Point your browser to [http://localhost:5000/]
