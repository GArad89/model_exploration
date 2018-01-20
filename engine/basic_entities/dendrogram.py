from .graph import DGraph

class Node:
    """implements the clusters that are in a cluster Dendrogram

        Attributes:
            child_indexes-(int list) the indexes of the current node's children in Dendrogram.node_list
            parent_index- (int) same as child indexes but for the parent.
            label- (string)the name of the cluster node
            subset-(networkx' node list) the graph nodes that are part of the current cluster node
            projected_graph- (networkx' graph)the projected graph of the current node cluster 
    """
    
    def __init__(self, parent=-1, subset=[],dgraph=None, label=None):
        if(parent==-1):
            if(label==None):
                self.label='root'

        self.parent_index=parent
        self.label=label if label is not None else ''
                
        self.subset=subset
        self.projected_graph=dgraph
        self.child_indexes=[]

    def add_child(self, child):
        self.child_indexes+=[child]

    def parent(self):
        return self.parent_index

    def child(self):
        return self.child_indexes

    def get_label(self):
        return self.label

    def vertices(self):
        return self.subset

    def set(self, subset,dgraph):
        self.subset=subset
        
    
class Dendrogram:
    """implements the cluster Dendrogram.

        Attributes:
            node_list-(Node list) list of the cluster nodes in the Dendrogram.
            dgraph- (networkx' MutilDigraph) the graph that is being explored. 
    """
    def __init__(self,dgraph):
        self.node_list=[]
        self.node_list+=[Node(None,list(dgraph.nodes()))] #root node
        self.dgraph=dgraph

    def add_node(self,node):
        self.node_list+=[node]

    def nodes(self):
        return self.node_list

    def add_child(self,parent,child): 
        self.node_list[parent].add_child(child)        

