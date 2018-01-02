from .cluster_abstract import Cluster
import networkx as nx
   
        
class MinimumCut(Cluster):

    @staticmethod
    def get_params():
        form = []
        schema = {}
        return schema, form
               
    def cluster(dgraph):
        cop=dgraph.dgraph.copy()
        cop=cop.to_undirected()
        cut_edges=nx.minimum_edge_cut(cop)

        cop.remove_edges_from(cut_edges)
        
        sub_graphs = nx.connected_component_subgraphs(cop)
        output=[]

        for sg in sub_graphs:
            output+=[sg.nodes()]

        return output
            





