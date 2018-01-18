from engine import clustering
import json


type_parsers = {
    'integer' : int,
    'number' : float,
    'string' : str,
}

def parse_parameters(parameters, schema):
    "parse parameters returned from form according to json schema. VERY LIMITED"
    parsed = {}
    for name, value in parameters.items():
        item_schema = schema[name]
        parser = type_parsers.get(item_schema['type'], None)
        if parser is None:
            raise Exception('unsupported schema type: ' + schema[name]['type'])
        real_value = parser(value)
        if 'enum' in item_schema:
            if real_value not in item_schema['enum']:
                raise Exception('Invalid enum value {} not in allowed values {}'.format(
                                    real_value, item_schema['enum']))
        parsed[name] = real_value
    return parsed


def get_algorithm_forms():
    """
    Returns a list of dictionaries, one for every algorithm, containing its name and json-form parameters
    e.g.
    [{'name': 'algo_1_name', 'form': {'schema' : json_schema, 'form': json_form} }, {'name' :algo_2_name, ...}, ...]
    """
    jsonlist = []
    algos = clustering.get_algorithms()
    for algo in algos:
        schema, form = algo.get_params()
        algo_form = {'name' : algo.__name__ , 'form' : {'schema' : schema, 'form' : form}}
        jsonlist += [algo_form]
    return jsonlist

def dendrogramToJSON(dendro):
    jsondata = {}
    jsondata['vertices'] = list(dendro.dgraph.nodes().items())
    jsondata['edges'] = list(dendro.dgraph.edges())
    #print(list(dendro.dgraph.edges()))
    clusters = []
    for index, node in enumerate(dendro.nodes()):
        clusters.append({
            'name' : node.get_label(),
            'inEdge' : node.parent(),
            'outEdge' : node.child(),
            'vertices' : list(node.vertices()),
            'id': 'cluster_{}'.format(index),
            })
    #print(clusters)
    jsondata['clusters'] = clusters

    jsondata['cluster_tree']= _build_cluster_tree(0,clusters)
    #print(jsondata['cluster_tree'])

    return jsondata

def _build_cluster_tree(index,cluster_list):
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
