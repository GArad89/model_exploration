from .cluster_abstract import Cluster
from engine.baisc_entities.graph import DGraph
import networkx as nx
   
        
class MinimumCut(Cluster):

    def getParams():
        form = []
        schema = {}
        return schema, form
               
    def cluster(dgraph):
        cop=dgraph.dgraph.copy()
        cop=cop.to_undirected()
        cut_edges=nx.minimum_edge_cut(cop)
        
        #print(cut_edges)
        cop.remove_edges_from(cut_edges)
        
        sub_graphs = nx.connected_component_subgraphs(cop)
        output=[]

        for sg in sub_graphs:
            output+=[sg.nodes()]

        return output
            





