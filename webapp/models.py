import os
from flask import current_app as app

from engine.graph import DGraph

EXTENSION = '.dot'

def _remove_ext(filename):
    "filename.ext -> filename"
    # rfind returns -1 on not found, so we'll get the full filename
    return filename[:filename.rfind('.')]

def _model_name_to_filename(model_name):
    return "{}{}".format(model_name, EXTENSION)

class Models:
    """
    Access to saved models (raw graphs).
    No caching.
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def list(self):
        "Return list of model ids"
        # all valid files transformed to model ids
        model_ids = [self.filename_to_model_name(filename) for filename in os.listdir(self.base_dir)
                            if self.allowed_filename(filename)]
        return model_ids

    def open(self, model_id):
        model_path = os.path.join(self.base_dir, _model_name_to_filename(model_id))
        return DGraph.read_dot(model_path)

    @staticmethod
    def allowed_filename(filename):
        "True if filename ends with '.dot'"
        return filename.endswith(EXTENSION)

    @staticmethod
    def filename_to_model_name(filename):
        # basename does  /path/to/file -> file
        return os.path.basename(_remove_ext(filename))

