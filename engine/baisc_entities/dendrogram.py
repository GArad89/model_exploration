from .graph import DGraph
import networkx as nx

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
        print()
        if(node.get_label()==None):
            self.label_by_sum_names(node)
        self.node_list+=[node]

    def nodes(self):
        return self.node_list

    def add_child(self,parent,child): 
        self.node_list[parent].add_child(child)

    def label_by_order(self,node):
        node.label='Node '+str(len(self.node_list))
    
    def label_by_sum_names(self, node):
        label_temp=[]
        #label_list=
        #print(label_list)
        for graph_node in node.subset:
            temp=node.projected_graph.dgraph.node[graph_node].get('label','')
            if temp:
                label_temp.append(str(temp))
            else: #TODO: something better
                label_temp.append(str(graph_node))

        #for edge in node.projected_graph.dgraph.edges():

        if label_temp:        
            node.label = "_".join(label_temp)
        else:
            self.label_by_order(node)

    def edges_by_sum_names(self,node):
        #TO DO
        pass
        

