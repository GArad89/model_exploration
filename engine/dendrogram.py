from graph import DGraph

class Node:
    parent_index=None
    child_indexes=[]
    rootindex=None
    label=None
    leafindexes=[]
    subset=[]
    projected_graph=None
    
    def __init__(self, parent=None, subset=[],dgraph=None):
        self.parent_index=parent
        self.subset=subset
        self.projected_graph=dgraph

    def add_child(self, child):
        self.child_indexes+=[child]

    def parent(self):
        return self.parent_index

    def child(self):
        return self.child_indexes

    def label(self):
        return self.label

    def vertices(self):
        return self.subset

    def set(self, subset,dgraph):
        self.subset=subset
        
    
class Dendrogram:
    dgraph=None
    node_list=[]
    def __init__(self,dgraph):
        self.node_list+=[Node(None,dgraph.nodes())] #root node
        self.dgraph=dgraph

    def add_node(self,node):
        self.node_list+=[node]

    def nodes(self):
        return self.node_list

    def add_child(self,parent,child):  #only used right after add_node. need to merge methods if there are no further uses
        self.node_list[parent].add_child(child)






