from .graph import DGraph
import networkx as nx

class Node:
    child_indexes=[]
    label=None
    subset=[]
    projected_graph=None
    
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
    dgraph=None
    node_list=[]
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

