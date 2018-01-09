from engine import clustering
import json


type_parsers = {
    'integer' : int,
    'number' : float,
    'text' : str,
}

def parse_parameters(parameters, schema):
    "parse parameters returned from form according to json schema"
    parsed = {}
    for name, value in parameters.items():
        parser = type_parsers.get(schema[name]['type'], None)
        if parser is None:
            raise Exception('unsupported schema type: ' + schema[name]['type'])
        parsed[name] = parser(value)
    return parsed


def createAlgoParamsJSON():
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

    jsondata['cluster_struct']=clusterBuild(0,clusters)
    #print(jsondata['cluster_struct'])

    return jsondata

def clusterBuild(index,cluster_list):
    node = {}

    node["name"] = cluster_list[index]['name']
    node["id"] = cluster_list[index]['id']

    children = []
    for child in cluster_list[index]['outEdge']:
        # recursively do this for children
        children.append(clusterBuild(child, cluster_list))
    # if there were children, add them
    if children:
        node['children'] = children

    return node
