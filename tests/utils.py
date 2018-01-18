
import os
import shutil
import numpy as np
import random

def project_root():
    "Get project root path"
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


RANDOM_SEED = 42
def test_init_seed():
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)


def delete_files_from_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)