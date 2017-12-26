from engine.clustering import *
from engine.clustering.cluster_abstract import Cluster
from engine.baisc_entities.dendrogram import *
import json

def createAlgoParamsJSON():
    
    jsonlist = []
    algos = Cluster.__subclasses__()
    for algo in algos:
        schema, form = algo.getParams()
        algo_form = {'name' : algo.__name__ , 'form' : {'schema' : schema, 'form' : form}}
        jsonlist += [algo_form]
    return jsonlist

def dendrogramToJSON(dendro):
    jsondata = {}
    jsondata['vertices'] = list(dendro.dgraph.nodes().items())
    jsondata['edges'] = list(dendro.dgraph.edges())
    #print(list(dendro.dgraph.edges()))
    clusters = []
    for node in dendro.nodes():
        clusters +=[ {'name' : node.get_label(), 'inEdge' : node.parent(), 'outEdge' : node.child(), 'vertices' : node.vertices()}]        
    #print(clusters)
    jsondata['clusters'] = clusters

    jsondata['cluster_struct']=clusterBuild(0,clusters)
    #print(jsondata['cluster_struct'])

    return jsondata

def clusterBuild(index,cluster_list):
    node = {}

    node["name"] = cluster_list[index]['name']

    children = []
    for child in cluster_list[index]['outEdge']:
        # recursively do this for children
        children.append(clusterBuild(child, cluster_list))
    # if there were children, add them
    if children:
        node['children'] = children

    return node
