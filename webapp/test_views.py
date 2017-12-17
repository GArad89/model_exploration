import pytest
from bs4 import BeautifulSoup
import os

from webapp import app

# don't log to file while running tests(?)
import logging
root_logger = logging.getLogger()
# remove all handlers that aren't right to stdout/err
handlers_to_remove = [h for h in root_logger.handlers if not isinstance(h, logging.StreamHandler) or isinstance(h, logging.FileHandler)]
for h in handlers_to_remove:
    root_logger.handlers.remove(h)


def cleanup_error(func, path, exc_info):
    import traceback
    print("Error deleting tree, when calling {func.__module__}.{func.__name__}({path})".format(func=func, path=path))
    traceback.print_exception(*exc_info)

# init app with dummy config, create test client and yield it, then clean up
@pytest.fixture
def client():
    import tempfile
    import shutil
    models_dir, results_dir = None, None
    try:
        models_dir = tempfile.mkdtemp(prefix='models_tmp')
        results_dir = tempfile.mkdtemp(prefix='results_tmp')
        app.config['MODELS_PATH'] = models_dir
        app.config['RESULTS_PATH'] = results_dir

        yield app.test_client()
    finally:
        # cleanup temp dirs, log errors instead of crashing
        shutil.rmtree(results_dir, onerror=cleanup_error)
        shutil.rmtree(models_dir, onerror=cleanup_error)


def get_model_list(soup):
    "parse returned html, get list of models from it"
    options = [str(option_tag.contents[0]) for option_tag in soup.find_all('option')]
    return options

# Note to first time readers: pytest sees the 'client' param here and so calls the client() fixture above
def test_model_choice(client):
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    options = get_model_list(soup)
    # blank models list, make sure we get a blank response
    assert options == ['Select File']

    # add a .dot file, verify that it shows up
    # add a non-.dot file, verify that it doesn't
    dot_name = 'a.dot'
    nondot_name = 'b.notdot'
    with open(os.path.join(app.config['MODELS_PATH'], dot_name), 'w'), \
         open(os.path.join(app.config['MODELS_PATH'], nondot_name), 'w'):
         pass

    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    options = get_model_list(soup)
    assert options == ['Select File', 'a'] # note no .dot suffix, no non-dot file

def test_model_upload(client):
    from io import BytesIO

    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    options = get_model_list(soup)
    # blank models list, make sure we get a blank response
    assert options == ['Select File']

    upload_elements = soup.find_all(lambda tag: tag.name=='input' and tag['type'] == 'file')
    assert len(upload_elements) == 1
    model_upload_element = upload_elements[0]
    model_upload_path = model_upload_element['data-url']

    # upload file with .dot
    ok_path = 'test.dot'
    bad_path = 'not_a.fileofdot'
    ok_contents = 'this is a test' 
    response = client.post(model_upload_path, data={model_upload_element['name'] : (BytesIO(ok_contents.encode('utf-8')), ok_path)})
    assert 200 <= response.status_code < 300
    response = client.post(model_upload_path, data={model_upload_element['name'] : (BytesIO(ok_contents.encode('utf-8')), bad_path)})
    assert 400 <= response.status_code < 500
    # get new models list

    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    options = get_model_list(soup)
    assert options == ['Select File', ok_path[:ok_path.rfind('.')]] # note no .dot suffix, no non-dot file

