from .graph import DGraph

class Node:
    parent_index=-1
    child_indexes=[]
    label=None
    subset=[]
    projected_graph=None
    
    def __init__(self, parent=None, subset=[],dgraph=None, label=None):
        if(parent==None):
            if(label==None):
                self.label='root'
        else:
            self.parent_index=parent
            self.label=label
                
        self.subset=subset
        self.projected_graph=dgraph
        self.child_indexes=[]

    def add_child(self, child):
        #print("child indexes of ",self.get_label()," ,is: ",self.child_indexes)
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
        if(node.get_label()==None):
            node.label='Node '+str(len(self.node_list))
        self.node_list+=[node]

    def nodes(self):
        return self.node_list

    def add_child(self,parent,child):  #only used right after add_node. need to merge methods if there are no further uses
        self.node_list[parent].add_child(child)






