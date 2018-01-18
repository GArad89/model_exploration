# README #

This repo contains model_exploration, a web-app to facilitate exploring software models represented as directed graphs (e.g. state machines), using hierarchical clustering with user input to choose the level of abstraction displayed,

### Table of Contents

**[How do I get set up?](#setup)**<br>
**[Configuration](#configuration)**<br>
**[Running](#configuration)**<br>
**[Contributing](#contributing)**<br>

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

#### Internal Dependencies

The web-app uses several dependencies that are on a CDN (see `webapp/templates/layout.html`):
* Bootstrap 4.0.0-beta.2
* jQuery 1.11

In addition, there are several dependencies we serve locally, usually because there is no version of them on a CDN:
* [jsonForm](https://github.com/joshfire/jsonform) - dynamic forms from schema (**Important**: We customized the library to work with bootstrap 4.0)
* d3-zoom - used for zoom & pan
* saveSvgAsPng
* viz.js - graphviz compiled to javascript via emscripten


### Configuration

`webapp_config.py` contains configuration for the web application:

* MODELS_PATH (default: PROJECT/models_dot/) - path to directory containing the .dot files representing models
* RESULTS_PATH (default: PROJECT/results/) - path to directory that will contain results of runs
* LOGGING_CONFIG (default: PROJECT/logging.conf) (YAML) - standard python logging configuration (log rotation, format, etc.). default stores logs in PROJECT_ROOT/logs/
* VIZJS_MAX_RAM (default: 128MB) - amount of RAM allocated for graphviz running on client machine in graph exploration page

### Running

* How to run tests

To run all tests run the following command from the main project folder: `py.test`

* How to run the server

`python3 run_webapp.py` will run the server

Point your browser to [http://localhost:5000/]


### Contributing

#### Clustering Algorithm

There are two steps to adding a clustering algorithm:
* Implemention - writing the algorithm
* Registering - hooking it up to the web-app

To implement the algorithm, inherit from the Cluster ABC (abstract base class) located at `./engine/clustering/cluster_abstract`

* `get_params()` - return jsonform-compatible (schema, form) tuple
* `cluster(dgraph)` - method accepting a DGraph and returning a list of list of nodes, each sub-list being a cluster

To be registered, modify the function `get_algorithms()` at `./engine/clustering/__init__.py` to also return your new clustering algorithm object

##### Accepting parameters

To accept parameters in the web-app, the clustering algorithm must describe what it requires using JSON-schema format. In addition, the input form must be described, referring to the schema.

The parameters you request are going to be passed as keyword arguments to the constructor of your clustering algorithm.

See `SpectralCluster.py` for a non-trivial example.

#### Labeling Algorithm

Similar to clustering algorithm: 

* Inherit from the GraphLabeler ABC (`engine/labeling/label.py`) 
* modify get_methods() in `engine/labeling/__init__.py` to also return your new class

