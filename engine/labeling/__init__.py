
from . import PrefixLabeler, TfIdfLabeler, PageRankLabeler, PathLabeler

def get_methods():
    "return list of all supported labeling method classes"
    return [PrefixLabeler.PrefixLabeler, TfIdfLabeler.TfIdfLabeler, PageRankLabeler.PageRankLabeler, PathLabeler.PathLabeler]

def get_labeling_method(name):
    "return class for specific labeling method"
    methods = get_methods()
    return methods[[method.__name__ for method in methods].index(name)]

def get_sources():
    return ['Both', 'Edges', 'Nodes']
