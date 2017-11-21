from abc import ABC, abstractmethod
from graph import DGraph
from sklearn.cluster import SpectralClustering
import numpy as np
import networkx as nx

    
class BnBNode():
    
    graph_node_list=[]
    upper_bound=None
    lower_bound=None
    weight=None
    parent_bnb_node=None
    child_bnb_nodes=[]
    
    def __init__(self,new_graph_node,upper_bound,lower_bound,weight,parent_bnb_node = None):
        
        self. graph_node_list=[new_graph_node]
        if (parent_bnb_node!=None):
            self.graph_node_list+=parent_bnb_node.graph_node_list
        
        self.upper_bound=upper_bound
        self.lower_bound=lower_bound
        self.weight=weight
        self.parent_bnb_node=parent_bnb_node

    def add_child(self, child_node):
        
        self.child_bnb_nodes+=child_node

        

class BnBSeachTree():
    
    weight_limit=-1
    node_list=[]
    live_nodes=[]
    leaf_list=[]
    
    def __init__(self,first_node,upper_bound,lower_bound,weight_limit):
        self.weight_limit=weight_limit
        node_list+=[BnBNode(first_node,upper_bound,lower_bound)]
        live_nodes+=[node_list[1]]
        
    def add_node(self, bnb_node,bnb_parent):
        node_list+=[bnb_node]
        live_nodes+=[bnb_node]
        bnb_parent.add_child(bnb_node)

    def kill_node(self,bnb_node):
        live_nodes.remove(bnb_node)

        
        
class Cluster(ABC):

    @abstractmethod
    def cluster(self, dgraph):
        """Returns a list of set of states for dgraph
        sets can be joint
        """

class BranchAndBoundCluster (Cluster):
    
    sorted_nodes_by_edge_weight=[]
    adj_mat=[]
    
    def getParams():
        return {},[] #TODO

    
    def cluster(self, dgraph):
        
        #adjacency matrix
        adj_mat =dgraph.adjacency_matrix()
        if("inNode" in dgraph.nodes()):
            adj_mat=np.delete(adj_mat, np.s_[-2::], 1)
            adj_mat=np.delete(adj_mat, np.s_[-2::], 0)

        upper_bound=0
        edge_weight_of_node=[0]*len(dgraph.nodes())
        for i in adj_mat:
            for j in adjmat[i]:
                upper_bound+=adjmat[i][j]    # just adding the weight of all the edges. should look for a tigher bound.
                edge_weight_of_node[i]+=adjmat[i][j]
                edge_weight_of_node[j]+=adjmat[i][j]

        lower_bound=0 #need to look for some kind of an estimate
        
        sorted_nodes_by_edge_weight=list(edge_weight_of_node)
        sorted_nodes_by_edge_weight.sort(reverse=True)
        for i in range(len(sorted_nodes_by_edge_weight)):
            sorted_nodes_by_edge_weight[i]=edge_weight_of_node.index(sorted_nodes_by_edge_weight[i])   #should give a list of node indexes sorted by the total weight of the node's edges
                
        first_node=sorted_nodes_by_edge_weight[0]
        bnbtree=BnBSeachTree(first_node,upper_bound,lower_bound,(len(dgraph.nodes())//2))

        while(len(bnbtree.live_nodes)>0):
                       
            current_live_node=bnbree.live_nodes[0]
            bnbtree.add_node(BnBNode(1,Calc_Upper_Bound([1]+current_live_node.graph_node_list), Lower_Bound([1]+current_live_node.graph_node_list))) #if the node is added to the subgraph (x_i=1)
            bnbtree.add_node(BnBNode(1,Calc_Upper_Bound([0]+current_live_node.graph_node_list), Lower_Bound([0]+current_live_node.graph_node_list))) #if the node is not added to the subgraph (x_i=0)
            bnbtree.kill_node(current_live_node)
            Check_Live(bnbtree)
                       

                       
    def Calc_Upper_Bound(graph_list):
        pass #TO DO
                             
    def Calc_Lower_Bound(graph_list):
        pass #TO DO

    def Check_Live(tree):     # run over the remaining BnB sub_problems and rejects according to the bounds
        pass #TO DO

        

class SpectralCluster (Cluster):

    def getParams():
        form = [{'key': 'n', 'type': 'text'},{'key': 'affinity', 'type': 'text'}]
        schema = {
            'n' : {'type': 'integer', 'title': 'number of clusters', 'minimum' : 2, 'required' : True},
            'affinity' : {'type': 'string', 'title': 'affinity'}
            }
        return schema, form
        




        
    def cluster(dgraph, n = 2, affinity='amg'):
        """
        just the basics required for the SpectralClustering algorithm for now.
        need to test what kind of output it gives.
        """
        #adjacency matrix
        adj_mat =dgraph.adjacency_matrix()
        if("inNode" in dgraph.nodes()):
            adj_mat=np.delete(adj_mat, np.s_[-2::], 1)
            adj_mat=np.delete(adj_mat, np.s_[-2::], 0)

        
        #SpectralClustering
        sc = SpectralClustering(n)
        sc.fit(adj_mat)
        result=sc.labels_

        #seperating the result list to lists for each cluster (1= the node is in the substae 0= the node is not in the state)
        output=[];
        for i in range(0,max(result)+1):
            temp_list=[];
            for j in range(0,len(result)):
                if result[j]!=i:
                    temp_list+=[0]
                else:
                    temp_list+=[1]
            output.append(temp_list)
        return output


