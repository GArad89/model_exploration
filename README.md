# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version

### How do I get set up? ###

* Dependencies

pydot implicitly requires python 3 <-> Tk integration. In Ubuntu/Debian, run:

`sudo apt install python3-tk`

Working git with ssh is required.

* Setup

Check out the git repository.

Install dependencies by running `pip3 install -r requirements.txt`

*NOTE:* Working git with ssh is required. GEM (Graph Embedding Methods) is installed from github directly since PyPI contains an outdated version at the moment (v0.1.12 at writing).

To develop and/or run unit tests, `pip3 install -r requirements-dev.txt` for additional, dev-only dependencies

To run all tests run the following command from the main project folder: `python -m unittest discover -s tests`

* Configuration

`webapp_config.py` contains configuration for the web application:

* MODELS_PATH [<project dir>/models_dot/] - path to directory containing the .dot files representing models
* RESULTS_PATH [<project dir>/results/] - path to directory that will contain results of runs
* LOGGING_CONFIG [<project dir>/logging.conf (YAML)] - standard python logging configuration (log rotation, format, etc.). default stores logs in <project dir>/logs/
Flask

* How to run tests
* Deployment instructions

`python3 run_webapp.py`

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact