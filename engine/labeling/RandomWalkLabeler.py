from .label import GraphLabeler,labeling_on_type
import networkx as nx
import numpy as np

np.set_printoptions(precision=5)

class RandomWalkLabeler(GraphLabeler):

    def n_important_nodes(self, subset, n):
        k = min(n, len(subset))
        subset_sorted = sorted(subset, key=lambda node: self.ranks[node], reverse=True)
        return subset_sorted[:k]

    def n_important_edges(self,subset_edges, n):
        print("chk3")
        edges_ranks = {}
        for edge in subset_edges:
            out_node = edge[0]
            out_node_rank = self.ranks[out_node]
            edges_ranks[(edge[0], edge[1])] = out_node_rank / len(self.graph.dgraph.out_edges())

        log.debug(edges_ranks)

        k = min(n, len(subset_edges))
        subset_sorted = sorted(subset_edges, key=lambda edge: edges_ranks[(edge[0], edge[1])], reverse=True)
        return subset_sorted[:k]
    
    def __init__(self, graph, dendrogram, source):
        super().__init__(graph, dendrogram, source)
        self.google_mat = nx.google_matrix(self.graph.dgraph)
        self.google_mat = np.array(self.google_mat)
        
    def label(self, label_size=3):
        ## X(G^t)=X   X=[1/n,1/n,...,1/n]
        n=len(self.graph.nodes())
        X = np.zeros(n)
        nodes = self.graph.dgraph.nodes()
        for i in range(n):
            X[i] = 1/n
        chk=False
        while(chk==False):
                temp=np.matmul(X, self.google_mat)
                chk=True
                for i in range(n):
                    if(abs(X[i]-temp[i])>0.001):
                       chk=False
                if(chk==False):
                    X=temp   
            
        X=temp
        self.ranks = dict(zip(nodes,X))

        for super_node in self.dendrogram.nodes():
            if self.source == labeling_on_type.NODES:
                chosen_nodes = self.n_important_nodes(super_node.subset, label_size)
                chosen_nodes_labels = [self.graph.node_attr(node, 'label') for node in chosen_nodes]
            elif (self.source == labeling_on_type.EDGES)or(self.source == labeling_on_type.EDGES_AND_NODES):
                print("chk3")
                chosen_edges = self.n_important_edges(super_node.projected_graph.edges(), label_size)
                print("chk3")
                chosen_labels = [self.graph.dgraph.edges[(edge[0], edge[1])].get('label','') for edge in chosen_edges]

            # super_node.label = super().shorten_label(','.join(chosen_nodes_labels))
            super_node.label = super().shorten_label(chosen_nodes_labels)
            print(super_node.label)
            
            

              
