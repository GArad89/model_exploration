from graph import DGraph

class Node:
    rootindex=None
    leafindexes=[]
    subset=[]
    projected_graph=None
    
    def __init__(self, root=None, subset=[],dgraph=None):
        self.rootindex=root
        self.subset=[]
        self.projected_graph=dgraph

    def add_leaf(self, leaf):
        self.leafindexes+=[leaf]

    def root(self):
        return self.rootindex

    def leaf(self):
        return self.leafindexes

    def set(self, subset,dgraph):
        self.subset=subset
        
    
class Dendrogram:
    dgraph=None
    nodes=[]
    def __init__(self,dgraph):
        self.nodes+=[Node(None,dgraph.nodes())] #root node
        self.dgraph=dgraph

    def add_node(self,node):
        self.nodes+=node

    def nodes(self):
        return self.nodes

    def add_leaf(self,root,leaf):
        self.nodes[root].add_leaf(leaf)






