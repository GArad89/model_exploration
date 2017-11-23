from cluster import *
from dendrogram import *
import json

def createAlgoParamsJSON():
    
    jsonlist = []
    algos = Cluster.__subclasses__()
    for algo in algos:
        schema, form = algo.getParams()
        algo_form = {'name' : algo.__name__ , 'form' : {'schema' : schema, 'form' : form}}
        jsonlist += [algo_form]
    return json.dumps(jsonlist)




def dendrogramToJSON(dendro):
    jsondata = {}
    jsondata['vertices'] = list(dendro.dgraph.nodes())
    jsondata['edges'] = list(dendro.dgraph.edges())
    #print(list(dendro.dgraph.edges()))
    clusters = []
    for node in dendro.nodes():
        clusters +=[ {'name' : node.get_label(), 'inEdge' : node.parent(), 'outEdge' : node.child(), 'vertices' : node.vertices()}]        
    #print(clusters)
    jsondata['clusters'] = clusters
    return json.dumps(jsondata)
