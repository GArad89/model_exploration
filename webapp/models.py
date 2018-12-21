import os
import json
import time
from flask import current_app as app
from werkzeug.utils import secure_filename

import logging

log = logging.getLogger(__name__)

from engine.basic_entities.graph import DGraph

EXTENSION = '.dot'

def _remove_ext(filename):
    "filename.ext -> filename"
    # rfind returns -1 on not found, so we'll get the full filename
    return filename[:filename.rfind('.')]

def _model_name_to_filename(model_name):
    return secure_filename("{}{}".format(model_name, EXTENSION))

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
        # basename does /path/to/file -> file
        return os.path.basename(_remove_ext(filename))

class Results:
    """
    Access to results of algorithm runs
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def list(self):
        "Return list of result ids"
        # all valid files transformed to model ids
        model_ids = [self.filename_to_result_name(filename) for filename in os.listdir(self.base_dir)
                            if self.allowed_filename(filename)]
        return model_ids

    def open(self, result_id):
        result_path =  self._result_id_to_path(result_id)
        with open(result_path) as result_file:
            return json.load(result_file)

    def save(self, result):
        """
        serialize result to json, save in new file, return id of the new file
        """
        serialized = json.dumps(result)
        current_time = time.time()
        lt = time.localtime(current_time)
        # format as YYYY_mm_dd__HH_MM_SS_XXX where XXX is milliseconds
        new_result_id = time.strftime("%Y_%m_%d__%H_%M_%S_") + '_{:03}'.format(int(current_time*1000) % 1000)
        result_path = self._result_id_to_path(new_result_id)
        log.info("Saving result into %s", result_path)
        # open create-only. This will disallow overwriting results due to parallel executions
        with open(result_path, 'x') as output_file:
            output_file.write(serialized)

        return new_result_id


    def _result_id_to_path(self, result_id):
        """
        convert result id to the matching file path
        """
        return os.path.join(self.base_dir, secure_filename(result_id + '.json'))

    @staticmethod
    def allowed_filename(filename):
        "True if filename ends with '.json'"
        return filename.endswith('.json')

    @staticmethod
    def filename_to_model_name(filename):
        # basename does  /path/to/file -> file
        return os.path.basename(_remove_ext(filename))

