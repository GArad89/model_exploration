from .cluster_abstract import Cluster
from ..baisc_entities.graph import DGraph
import numpy as np
import networkx as nx
import copy

#Branch and Bound not working for now

class BnBNode():
    


    
    def __init__(self,new_graph_node,is_accepted, LB,parent_bnb_node = None):
        self.accepted=[]
        self.rejected=[]
        self.checked=[]
        self.LB=None
        self.weight=0
        self.parent_bnb_node=None
        self.child_bnb_nodes=[]
        
        if (parent_bnb_node!=None):
            self.accepted+=parent_bnb_node.accepted
            self.rejected+=parent_bnb_node.rejected
            self.weight=parent_bnb_node.weight
            self.checked+=parent_bnb_node.checked

        self.LB=LB
        self.parent_bnb_node=parent_bnb_node
        if(is_accepted==True):
            self.weight+=1
            self.accepted+=[new_graph_node]
        else:
           self.rejected+=[new_graph_node]

        self.checked+=[new_graph_node]

    def add_child(self, child_node):
        
        self.child_bnb_nodes+=[child_node]

        

class BnBSearchTree():

    graph=None
    sorted_graph_nodes=None
    weight_limit=-1
    node_list=[]
    live_nodes=[]
    upper_bound=-1
    best_solution=None
    
    def __init__(self,dgraph):
        self.weight_limit=len(dgraph.nodes())//2+1
        self.graph=dgraph
        self.sorted_graph_nodes=Sort_Nodes(dgraph)
        self.node_list+=[BnBNode(self.sorted_graph_nodes[0],True, 0)]
        self.upper_bound=dgraph.dgraph.size()
        self.live_nodes+=[self.node_list[0]]
        #print(self.live_nodes[0].checked)
        
    def add_node(self, bnb_node,bnb_parent):
        self.node_list+=[bnb_node]
        self.live_nodes+=[bnb_node]
       # print(bnb_node.checked)
        self.live_nodes.sort(key=lambda x: x.LB)
        bnb_parent.add_child(bnb_node)
        if((len(self.sorted_graph_nodes)==len(bnb_node.checked))or(len(bnb_node.accepted)==self.weight_limit)or(len(bnb_node.rejected)==self.weight_limit)):
           #bnb_node.LB=check_final_cut(bnb_node,self.graph)
           if(bnb_node.LB<self.upper_bound):
               self.best_solution=bnb_node
               self.upper_bound=bnb_node.LB
           self.kill_node(bnb_node)

    def kill_node(self,bnb_node):
        self.live_nodes.remove(bnb_node)

        
        


class BranchAndBoundCluster (Cluster):
    
    sorted_nodes_by_edge_weight=[]
    adj_mat=[]
    
    def getParams():
        return {},[] #TODO

    
    def cluster(self, dgraph,target,heru_LB,heru_UP,heru_order):
        
        bnb_tree=BnBSearchTree(dgraph)
        current_upper_bound=bnb_tree.upper_bound
        while(len(bnb_tree.live_nodes)>0):
            live_node=bnb_tree.live_nodes[0]
            if(len(live_node.checked)<=len(bnb_tree.sorted_graph_nodes)):   
                graph_node=bnb_tree.sorted_graph_nodes[len(live_node.checked)]
                #print(live_node.accepted)
                bnb_tree.add_node(BnBNode(graph_node,True,LB_Greedy_Simple(bnb_tree.graph,live_node,graph_node,True),live_node),live_node)
                bnb_tree.add_node(BnBNode(graph_node,False,LB_Greedy_Simple(bnb_tree.graph,live_node,graph_node,False),live_node),live_node)
            bnb_tree.kill_node(live_node)
            if(bnb_tree.upper_bound<current_upper_bound):
                current_upper_bound=bnb_tree.upper_bound
                Check_Live(bnb_tree)
        Print_Sol(bnb_tree)
        print(bnb_tree.best_solution. accepted)
        return bnb_tree.best_solution. accepted
        
def Check_Live(tree):     # run over the remaining BnB sub_problems and rejects according to the bounds
    rejected=[]                     
    for node in tree.live_nodes:
        if(node.LB>tree.upper_bound):
            rejected+=[node]
    for node in rejected:
        tree.kill_node(node)

def LB_Greedy_Simple(dgraph, bnb_node, graph_node, is_accepted):
    graph_edges=dgraph.edges()
    
    edge_list=[]
    for edge in graph_edges:
        if(edge[0]==graph_node):
            
            edge_list+=[edge[1]]
        elif((edge[1]==graph_node)):
            edge_list+=[edge[0]]
    LB=bnb_node.LB
    
    for edge in edge_list:
        
        if(bnb_node.accepted.count(edge)>0):
            LB+=(1-is_accepted)
        if(bnb_node.rejected.count(edge)>0):
            LB+=is_accepted
    return LB
            
def Sparset_Cut_Target(bound,graph_node_num):
    return bound/graph_node_num

def Quotient_Cut_Target(bound, dgraph_maybe):
    pass #TO DO


def Sort_Nodes(dgraph):
    deg_dict=dgraph.dgraph.degree(dgraph.nodes())
    
    sorted_nodes_tuple=sorted(deg_dict, key=lambda tup: tup[1])
    sorted_nodes_tuple.reverse()
    sorted_nodes=[]
    for tup in sorted_nodes_tuple:
        sorted_nodes+=[tup[0]]
    #print(sorted_nodes)
    return sorted_nodes

def Print_Sol(bnbtree):
    for node in bnbtree.node_list:
        print("accepted: ")
        print(node.accepted)
        print("rejected: ")
        print(node.rejected)
        print("LB: ")
        print(node.LB)

def check_final_cut(bnbnode,dgraph):
    if(len(bnbnode.accepted)>=len(bnbnode.rejected)):
       added_list=bnbnode.accepted
    else:
       added_list=bnbnode.rejected
    for node in dgraph.nodes():
       if(bnbnode.checked.count(node)==0):
           added_list+=[node]
       
    graph_edges=dgraph.edges()
    
    LB=0
    for edge in graph_edges:
        if((bnbnode.accepted.count(edge[0])>0)and(bnbnode.rejected.count(edge[1])>0)):
           LB+=1
        else:
           if((bnbnode.accepted.count(edge[1])>0)and(bnbnode.rejected.count(edge[0])>0)):
              LB+=1
        
    return LB


        ## old code##
    """
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

        LB=0 #need to look for some kind of an estimate
        
        sorted_nodes_by_edge_weight=list(edge_weight_of_node)
        sorted_nodes_by_edge_weight.sort(reverse=True)
        for i in range(len(sorted_nodes_by_edge_weight)):
            sorted_nodes_by_edge_weight[i]=edge_weight_of_node.index(sorted_nodes_by_edge_weight[i])   #should give a list of node indexes sorted by the total weight of the node's edges
                
        first_node=sorted_nodes_by_edge_weight[0]
        bnbtree=BnBSeachTree(first_node,upper_bound,LB,(len(dgraph.nodes())//2))

        while(len(bnbtree.live_nodes)>0):
                       
            current_live_node=bnbree.live_nodes[0]
            bnbtree.add_node(BnBNode(1,Calc_Upper_Bound([1]+current_live_node.graph_node_list), LB([1]+current_live_node.graph_node_list))) #if the node is added to the subgraph (x_i=1)
            bnbtree.add_node(BnBNode(1,Calc_Upper_Bound([0]+current_live_node.graph_node_list), LB([0]+current_live_node.graph_node_list))) #if the node is not added to the subgraph (x_i=0)
            bnbtree.kill_node(current_live_node)
            Check_Live(bnbtree)
                       

                       
    def Calc_Upper_Bound(graph_list):
        pass #TO DO
        """                     


        

