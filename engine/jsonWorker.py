from .cluster import *
from .dendrogram import *
import json


def createAlgoParamsJSON():
    jsonlist = []
    algos = Cluster.__subclasses__()
    for algo in algos:
        schema, form = algo.getParams()
        algo_form = {'name': algo.__name__, 'form': {'schema': schema, 'form': form}}
        jsonlist += [algo_form]
    return json.dumps(jsonlist)


def dendrogramToJSON(dendro):
    jsondata = {}
    jsondata['vertices'] = list(dendro.dgraph.nodes())
    jsondata['edges'] = list(dendro.dgraph.edges())
    # print(list(dendro.dgraph.edges()))
    clusters = []
    for node in dendro.nodes():
        clusters += [
            {'name': node.get_label(), 'inEdge': node.parent(), 'outEdge': node.child(), 'vertices': node.vertices()}]
        # print(clusters)
    jsondata['clusters'] = clusters
    result = jsondata['clusters']
    jsondata['cluster_struct'] = clusterBuild(0, result)
    # print(jsondata['cluster_struct'])

    return jsondata

# TO-DO new clusterBuild function based on new dendrogram class
''' old code:
def clusterBuild(index, cluster_list):
    text = ""
    x = '"'
    text = text + '{' + '\n' + """"name": """ + x + cluster_list[index]['name'] + x
    for j in range(len(cluster_list[index]['outEdge'])):
        text = text + ','
        if (j == 0):
            text = text + """\n"children": ["""
        text = text + '\n' + clusterBuild(cluster_list[index]['outEdge'][j], cluster_list)
    if (len(cluster_list[index]['outEdge']) > 0):
        text = text + """\n] \n}"""
    else:
        text = text + """ \n}"""
    return text
'''
