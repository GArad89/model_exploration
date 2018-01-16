
import os
import numpy as np
import random

def project_root():
    "Get project root path"
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

RANDOM_SEED = 42
def test_init_seed():
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)