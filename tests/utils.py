
import os

def project_root():
    "Get project root path"
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))