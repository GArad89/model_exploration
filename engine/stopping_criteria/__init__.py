from .stop_criteria import SizeCriteria, InOutDegreeCriteria, CyclometricCriteria
def get_criteria():
    "return list of stopping criteria classes"
    return [SizeCriteria, InOutDegreeCriteria, CyclometricCriteria]

def get_stopping_criterion(name):
    "return class for specific stopping criterion"
    criteria = get_criteria()
    return criteria[[criterion.__name__ for criterion in criteria].index(name)]