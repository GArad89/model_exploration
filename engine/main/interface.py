from engine.clustering import get_cluster_algorithm
from engine.stopping_criteria import get_stopping_criterion
from engine.labeling import get_labeling_method
from .partition import partition
import logging

log = logging.getLogger(__name__)

import importlib

from engine import clustering
import json


def _build_cluster_tree(index, cluster_list):
    "turn cluster graph to tree"
    node = {}

    node["name"] = cluster_list[index]['name']
    node["id"] = cluster_list[index]['id']

    children = []
    for child in cluster_list[index]['outEdge']:
        # recursively do this for children
        children.append(_build_cluster_tree(child, cluster_list))
    # if there were children, add them
    if children:
        node['children'] = children

    return node

def _serialize_dendrogram(dendrogram):
    """
    Serialize a dendrogram to a json-friendly format
    :param dendrogram: engine.basic_entities.dendrogram.Dendrogram
    :returns: json-friendly serialization of the dendrogram(dictionary of lists)
    """

    jsondata = {}
    jsondata['vertices'] = list(dendrogram.dgraph.nodes().items())
    jsondata['edges'] = list(dendrogram.dgraph.edges())
    clusters = []
    for index, node in enumerate(dendrogram.nodes()):
        clusters.append({
            'name' : node.get_label(),
            'inEdge' : node.parent(),
            'outEdge' : node.child(),
            'vertices' : list(node.vertices()),
            'id': 'cluster_{}'.format(index),
            })
    jsondata['clusters'] = clusters
    jsondata['cluster_tree']= _build_cluster_tree(0,clusters)

    return jsondata


def get_algorithm_forms():
    """
    :return: Returns a list of dictionaries, one for every algorithm, containing its name and json-form parameters. e.g. [{'name': 'algo_1_name', 'form': {'schema' : json_schema, 'form': json_form} }, {'name' :algo_2_name, ...}, ...]
    """
    jsonlist = []
    algos = clustering.get_algorithms()
    for algo in algos:
        schema, form = algo.get_params()
        algo_form = {'name' : algo.__name__ , 'form' : {'schema' : schema, 'form' : form}}
        jsonlist += [algo_form]
    return jsonlist


_type_parsers = {
    'integer' : int,
    'number' : float,
    'string' : str,
}

def parse_parameters(parameters, schema):
    "parse parameters returned from form according to json schema. VERY LIMITED"
    parsed = {}
    for name, value in parameters.items():
        item_schema = schema[name]
        parser = _type_parsers.get(item_schema['type'], None)
        if parser is None:
            raise Exception('unsupported schema type: ' + schema[name]['type'])
        real_value = parser(value)
        if 'enum' in item_schema:
            if real_value not in item_schema['enum']:
                raise Exception('Invalid enum value {} not in allowed values {}'.format(
                                    real_value, item_schema['enum']))
        parsed[name] = real_value
    return parsed


def run_algorithm(graph, algo_name, params, stopping_criterion, stopping_parameter, labeling_method, labeling_source):
    #parsing from string + params to algo object
    algo_class = get_cluster_algorithm(algo_name) #we want the algorithm class
    algo = algo_class(**params) #now we have an object
    
    stopping_criterion_class = get_stopping_criterion(stopping_criterion)
    stopping_criterion = stopping_criterion_class(stopping_parameter) # now we have an object
    dendrogram = partition(graph, algo, stopping_criterion)

    labeler_class = get_labeling_method(labeling_method)
    labeler = labeler_class(graph, dendrogram, labeling_source)
    labeler.label()

    log.info(len(dendrogram.nodes()))

    for super_node in dendrogram.nodes():
        log.info(super_node.label)

    return _serialize_dendrogram(dendrogram)

