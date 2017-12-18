from .cluster_abstract import Cluster
from ..baisc_entities.graph import DGraph
import numpy as np
import networkx as nx
import copy
import __main__
from ..linear_programming.lin_prog_solver import *

def Sparset_Cut_Target(bound,graph_node_num):
    return bound/graph_node_num

def LB_Greedy_Simple(dgraph, bnb_node):
    graph_edges=dgraph.edges()
    is_accepted=True
    
    if(bnb_node.parent_bnb_node==None):
        return 0
    
    edge_list=[]
    
    for node in bnb_node.checked:
        if node not in bnb_node.parent_bnb_node.checked:
            graph_node=node
            break
        
    if graph_node in bnb_node.accepted:
        is_accepted=True
    else:
        is_accepeted=False
    
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

def Sort_Nodes_byDegree(dgraph, bnb_node=None):  #bnb_node added so Sort by degrees input variables will match other sort heruistics.  
    deg_dict=dgraph.dgraph.degree(dgraph.nodes())
    
    sorted_nodes_tuple=sorted(deg_dict, key=lambda tup: tup[1])
    sorted_nodes_tuple.reverse()
    sorted_nodes=[]
    
    for tup in sorted_nodes_tuple:
        sorted_nodes+=[tup[0]]
        
    print(sorted_nodes)
    return sorted_nodes

class BnBNode():
    

   
    def __init__(self,new_graph_node,is_accepted, heru_dict,dgraph,parent_bnb_node = None):
        self.accepted=[]
        self.rejected=[]
        self.checked=[]
        self.dgraph=dgraph
        self.weight=0
        self.LB=0
        self.UB=None
        self.parent_bnb_node=None
        self.child_bnb_nodes=[]
        
        if (parent_bnb_node!=None):
            self.accepted+=parent_bnb_node.accepted
            self.rejected+=parent_bnb_node.rejected
            self.weight=parent_bnb_node.weight
            self.checked+=parent_bnb_node.checked
            self.LB=parent_bnb_node.LB

        self.parent_bnb_node=parent_bnb_node
        if(is_accepted==True):
            self.weight+=1
            self.accepted+=[new_graph_node]
        else:
           self.rejected+=[new_graph_node]

        self.checked+=[new_graph_node]
        self.LB=heru_dict['heru_LB'](dgraph,self)
        self.UB=None
        
    def add_child(self, child_node):
        
        self.child_bnb_nodes+=[child_node]

        

class BnBSearchTree():

    graph=None
    initial_sorted_graph_nodes=None
    weight_limit=-1
    node_list=[]
    live_nodes=[]
    upper_bound=-1
    best_solution=None
    
    def __init__(self,dgraph,heru_dict):
        self.weight_limit=len(dgraph.nodes())//2+1  ##anything more than half of the nodes+1 will only need to symmetrical solutions
        self.graph=dgraph
        self.sorted_graph_nodes=heru_dict['heru_order'](dgraph)
        self.node_list+=[BnBNode(self.sorted_graph_nodes[0],True,heru_dict,dgraph)]
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
           bnb_node.LB=check_final_cut(bnb_node,self.graph)
           if(bnb_node.LB<self.upper_bound):
               self.best_solution=bnb_node
               self.upper_bound=bnb_node.LB
           self.kill_node(bnb_node)

    def kill_node(self,bnb_node):
        self.live_nodes.remove(bnb_node)

    def Check_Live(self):     # run over the remaining BnB sub_problems and rejects according to the bounds
        rejected=[]
        if(self.upper_bound>0):
            for node in self.live_nodes:
                if(node.LB>self.upper_bound):
                    rejected+=[node]
            for node in rejected:
                self.kill_node(node)    
        


class BranchAndBoundCluster (Cluster):
    
    sorted_nodes_by_edge_weight=[]
    adj_mat=[]
    
    def getParams():
        return {},[] #TODO

    
    def cluster(self, dgraph,target=Sparset_Cut_Target,heru_LB=LB_Greedy_Simple,heru_UB=None,heru_order=Sort_Nodes_byDegree):

        heru_dict={'target':target,'heru_LB':heru_LB,'heru_UB':heru_UB,'heru_order':heru_order}
        bnb_tree=BnBSearchTree(dgraph,heru_dict)
        current_upper_bound=bnb_tree.upper_bound
        while(len(bnb_tree.live_nodes)>0):
            live_node=bnb_tree.live_nodes[0]
            if(len(live_node.checked)<=len(bnb_tree.sorted_graph_nodes)):   
                graph_node=bnb_tree.sorted_graph_nodes[len(live_node.checked)]
                #print(live_node.accepted)
                bnb_tree.add_node(BnBNode(graph_node,True,heru_dict,dgraph,live_node),live_node)
                bnb_tree.add_node(BnBNode(graph_node,False,heru_dict,dgraph,live_node),live_node)
            bnb_tree.kill_node(live_node)
            if(bnb_tree.upper_bound<current_upper_bound):
                current_upper_bound=bnb_tree.upper_bound
            bnb_tree.Check_Live()
        main_name=__main__.__file__.split('\\')
        if(main_name[-1]=='BnB_test.py'):
            Print_Sol(bnb_tree)
            print(bnb_tree.best_solution. accepted)
        return [bnb_tree.best_solution. accepted,bnb_tree.best_solution. rejected]
        




def LB_lps(dgraph,bnb_node):
     partial_assignment_dict={}
     for node in bnb_node.accepted:
         partial_assignment_dict[node]=1
     for node in bnb_node.rejected:
         partial_assignment_dict[node]=0
     return lps.compute_lower_bound(dgraph)
            


def Quotient_Cut_Target(bound, dgraph_maybe):
    pass #TO DO




def Print_Sol(bnbtree):
    print("bnb search tree holds "+str(len(bnbtree.node_list))+" nodes")
    for node in bnbtree.node_list:
        print("accepted: ")
        print(node.accepted)
        print("rejected: ")
        print(node.rejected)
        print("LB: ")
        print(node.LB)


def check_final_cut(bnbnode,dgraph):
    if(len(bnbnode.accepted)>=len(bnbnode.rejected)):
       added_list=bnbnode.rejected
    else:
       added_list=bnbnode.accepted
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


        

