from .cluster_abstract import Cluster
import networkx as nx
   
        
class MinimumCut(Cluster):
    """ Returns a minimum cut partition of the input dgraph.
        this clustering method uses networkx minimum_edge_cut method
        in order to get the cut.
        please note that the other clustering methods return a sparset cut and not a minimum cut.
        the minimum cut most of the time will partition the graph to one node in one cluster and the rest of the graph in the 2nd cluster.
    """

    @staticmethod
    def get_params():
        form = []
        schema = {}
        return schema, form

    def cluster(self, dgraph):

        ## get edges in the cut
        cop = super().to_undirected(dgraph.dgraph)
        cut_edges=nx.minimum_edge_cut(cop)

        ## remove edges in the cut and get connected subgraphs
        cop.remove_edges_from(cut_edges) 
        sub_graphs = nx.connected_component_subgraphs(cop)
        output=[]

        for sg in sub_graphs:
            output+=[list(sg.nodes())]

        return output
            





