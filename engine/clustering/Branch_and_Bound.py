from .cluster_abstract import Cluster
from engine.baisc_entities.graph import DGraph
import numpy as np
import networkx as nx
import copy
from engine.linear_programming.lin_prog_solver import *

def sparset_cut_target(bound,graph_node_num):
    return bound/graph_node_num

def lower_bound_lps(dgraph,bnb_node):
     if(len(bnb_node.checked)==len(dgraph.nodes())): return check_final_cut(bnb_node,dgraph)
     a,bnb_node.res= LPS().solve_LB(dgraph.dgraph)
     return a

def lower_bound_lps_simple(dgraph,bnb_node):
     if(bnb_node.parent_bnb_node==None):
         a,bnb_node.res= LPS().solve_LB(dgraph.dgraph)
         return a
     return lower_bound_greedy_simple(dgraph,bnb_node)

def upper_bound_lps_simple(dgraph,bnb_node,new_graph_node,is_accepted):
    if(bnb_node.parent_bnb_node==None): return upper_bound_lps(dgraph,bnb_node,new_graph_node,is_accepted)
    if((new_graph_node in bnb_node.parent_bnb_node.relaxed_a)and(is_accepted==False))or((new_graph_node in bnb_node.parent_bnb_node.relaxed_r)and(is_accepted)):
        bnb_node.relaxed_a=bnb_node.parent_bnb_node.relaxed_a
        bnb_node.relaxed_r=bnb_node.parent_bnb_node.relaxed_r
        if (is_accepted==False):
            bnb_node.relaxed_a.remove(new_graph_node)
            bnb_node.relaxed_r+=[new_graph_node]
        else:
            bnb_node.relaxed_r.remove(new_graph_node)
            bnb_node.relaxed_a+=[new_graph_node]
    else: return bnb_node.parent_bnb_node.UB
    temp= copy.deepcopy(bnb_node)
    temp.accepted=bnb_node.relaxed_a
    temp.rejected=bnb_node.relaxed_r
    return check_final_cut(temp,dgraph)
    
def upper_bound_lps(dgraph,bnb_node,new_graph_node,is_accepted):
    if(bnb_node.parent_bnb_node==None):
        bnb_node.relaxed_a,bnb_node.UB=LPS().solve_UB(dgraph.dgraph, bnb_node.res,{})
    else:
     if((new_graph_node in bnb_node.parent_bnb_node.relaxed_a)and(is_accepted==False))or((new_graph_node in bnb_node.parent_bnb_node.relaxed_r)and(is_accepted)):
         for node in bnb_node.accepted:
            bnb_node.partial_assignment_dict[node]=1
         for node in bnb_node.rejected:
            bnb_node.partial_assignment_dict[node]=0
         print(bnb_node.partial_assignment_dict)
         if(len(bnb_node.partial_assignment_dict)==len(dgraph.nodes())):
            bnb_node.LB=check_final_cut(bnb_node,dgraph)
            return bnb_node.LB
         if(len(bnb_node.partial_assignment_dict)==len(dgraph.nodes())-1):
            bnb_node.LB=lower_bound_greedy_simple(dgraph, bnb_node) 
            return bnb_node.LB
         bnb_node.relaxed_a,bnb_node.UB=LPS().solve_UB(dgraph.dgraph,bnb_node.bnb_node.res,partial_assignment_dict)
     else:
        bnb_node.relaxed_a=bnb_node.parent_bnb_node.relaxed_a
        bnb_node.relaxed_r=bnb_node.parent_bnb_node.relaxed_r
        bnb_node.UB=bnb_node.parent_bnb_node.UB

    if(len(bnb_node.relaxed_r)==0):
        for node in dgraph.nodes():
            if node not in bnb_node.relaxed_a: bnb_node.relaxed_r+=[node]
    #print("UB is "+str(bnb_node.UB))
    return bnb_node.UB
  

def upper_bound_greedy_simple(dgraph,bnb_node,new_graph_node,is_accepted):
    #not an actual upper bound, it replace the sorting by upper bound to sorting by lowerbound
    #the input is only in order to have the same input as upper_bound_lps
    return bnb_node.LB

def lower_bound_greedy_simple(dgraph, bnb_node):
    graph_edges = dgraph.edges()
    is_accepted = True
    
    if(bnb_node.parent_bnb_node == None): return 0
    
    edge_list = []
    graph_node=None
    for node in bnb_node.checked:
        if node not in bnb_node.parent_bnb_node.checked:
            graph_node=node
            break
        
    is_accepted = (graph_node in bnb_node.accepted)
    
    for edge in graph_edges:
        #print()
        if(edge[0]==graph_node):
            edge_list+=[[edge[1],edge[2].get('weight',1)]]
        elif((edge[1]==graph_node)):
            edge_list+=[[edge[0],edge[2].get('weight',1)]]
            
    LB=bnb_node.LB
    LB*=(len(dgraph.nodes())-len(bnb_node.checked)+2*min(len(bnb_node.parent_bnb_node.accepted),len(bnb_node.parent_bnb_node.rejected)))
    
    for edge in edge_list:
        #print(edge)
        if (bnb_node.accepted.count(edge[0])>0): LB+=(1-is_accepted)*int(edge[1])
        if (bnb_node.rejected.count(edge[0])>0): LB+=is_accepted*int(edge[1])
    return LB/(len(dgraph.nodes())-len(bnb_node.checked)+2*min(len(bnb_node.accepted),len(bnb_node.rejected)))

def sort_nodes_bydegree(dgraph, bnb_node=None):  #bnb_node added so Sort by degrees input variables will match other sort heruistics.  
    deg_dict=dgraph.dgraph.degree(dgraph.nodes())
    
    sorted_nodes_tuple=sorted(deg_dict, key=lambda tup: tup[1])
    sorted_nodes_tuple.reverse()
    sorted_nodes=[]
    
    for tup in sorted_nodes_tuple:
        sorted_nodes+=[tup[0]]
        
    #print(sorted_nodes)
    return sorted_nodes

class BnBNode():
    

   
    def __init__(self,new_graph_node,is_accepted, heru_dict,dgraph,parent_bnb_node = None):
        self.accepted=[]
        self.rejected=[]
        self.checked=[]
        self.relaxed_a=[]
        self.relaxed_r=[]
        self.res=None
        self.dgraph=dgraph
        self.weight=0
        self.LB=0
        self.UB=None
        self.parent_bnb_node=None
        self.child_bnb_nodes=[]
        self.partial_assignment_dict={}
        
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
        self.UB=heru_dict['heru_UB'](dgraph,self,new_graph_node,is_accepted)
        
    def add_child(self, child_node):
        
        self.child_bnb_nodes+=[child_node]

        

class BnBSearchTree():

    graph=None
    initial_sorted_graph_nodes=None
    weight_limit=-1
    node_list=[]
    live_nodes=[]
    best_sol_cut=0
    best_solution=None
    
    def __init__(self,dgraph,heru_dict):
        self.weight_limit=len(dgraph.nodes())//2+1  ##anything more than half of the nodes+1 will only need to symmetrical solutions
        self.graph=dgraph
        self.sorted_graph_nodes=heru_dict['heru_order'](dgraph)
        self.node_list+=[BnBNode(self.sorted_graph_nodes[0],True,heru_dict,dgraph)]
        for edge in self.graph.edges():
            self.best_sol_cut+=int(edge[2].get('weight',1))
        self.live_nodes+=[self.node_list[0]]
        #print(self.live_nodes[0].checked)
        
    def add_node(self, bnb_node,bnb_parent):
        self.node_list+=[bnb_node]
        self.live_nodes+=[bnb_node]
       # print(bnb_node.checked)
        self.live_nodes.sort(key=lambda x: (x.UB,x.LB,len(x.checked)))
        bnb_parent.add_child(bnb_node)
        if((len(self.sorted_graph_nodes)==len(bnb_node.checked))or(len(bnb_node.accepted)==self.weight_limit)or(len(bnb_node.rejected)==self.weight_limit)):
           bnb_node.LB=check_final_cut(bnb_node,self.graph)
           if(bnb_node.LB<=self.best_sol_cut):
               self.best_solution=bnb_node
               self.best_sol_cut=bnb_node.LB
              # print(self.best_sol_cut)
           self.kill_node(bnb_node)

    def kill_node(self,bnb_node):
        self.live_nodes.remove(bnb_node)

    def _check_live(self):     # run over the remaining BnB sub_problems and rejects according to the bounds
        rejected=[]
        if((self.best_sol_cut>0)and(self.best_solution!=None)):
            for node in self.live_nodes:
                if(node.LB>self.best_sol_cut): rejected+=[node]
            for node in rejected:
                self.kill_node(node)    
        


class BranchAndBoundCluster (Cluster):
    
    sorted_nodes_by_edge_weight=[]
    adj_mat=[]
    
    def __init__(self,target=sparset_cut_target,heru_LB=lower_bound_greedy_simple,heru_UB=upper_bound_greedy_simple,heru_order=sort_nodes_bydegree):
        self.target = target
        self.heru_LB = heru_LB
        self.heru_UB = heru_UB
        self.heru_order = heru_order


    @staticmethod
    def get_params():
        return {},[] #TODO

    
    def cluster(self, dgraph, debug_print=False):
        #print(dgraph.nodes())
        heru_dict={'target':self.target,'heru_LB':self.heru_LB,'heru_UB':self.heru_UB,'heru_order':self.heru_order}
        bnb_tree=BnBSearchTree(dgraph,heru_dict)
        current_best_sol_cut=bnb_tree.best_sol_cut
        
        while(len(bnb_tree.live_nodes)>0):
            live_node=bnb_tree.live_nodes[0]
            
            if(len(live_node.checked)<=len(bnb_tree.sorted_graph_nodes)):   
                graph_node=bnb_tree.sorted_graph_nodes[len(live_node.checked)]
               # print(live_node.accepted)
                #print(live_node.LB)
                bnb_tree.add_node(BnBNode(graph_node,True,heru_dict,dgraph,live_node),live_node)
                bnb_tree.add_node(BnBNode(graph_node,False,heru_dict,dgraph,live_node),live_node)
                
            bnb_tree.kill_node(live_node)
            if(bnb_tree.best_sol_cut<current_best_sol_cut): current_best_sol_cut=bnb_tree.best_sol_cut
            bnb_tree._check_live()
            
        #main_name=__main__.__file__.split('\\')
        if debug_print:
            print("bnb search tree holds "+str(len(bnb_tree.node_list))+" nodes")
##            Print_Sol(bnb_tree)
            print(bnb_tree.best_solution. accepted)
            print(bnb_tree.best_solution. rejected)
            print("LB: "+str(bnb_tree.best_solution.LB))
            
        return [bnb_tree.best_solution. accepted,bnb_tree.best_solution. rejected]
        




def Quotient_Cut_Target(bound, dgraph_maybe):
    pass #TO DO




def Print_Sol(bnbtree):
    
    for node in bnbtree.node_list:
        print("accepted: ")
        print(node.accepted)
        print("rejected: ")
        print(node.rejected)
        print("LB: ")
        print(node.LB)


def check_final_cut(bnbnode,dgraph):
    if(len(bnbnode.accepted)>=len(bnbnode.rejected)): added_list=bnbnode.rejected
    else: added_list=bnbnode.accepted
    temp_list=[]
    for node in dgraph.nodes():
       if(node not in bnbnode.checked): temp_list+=[node]
    added_list+=temp_list
       
    graph_edges=dgraph.dgraph.edges(data=True)
    
    LB=0
    #if((min(len(bnbnode.accepted),len(bnbnode.rejected)))>0): LB*=(min(len(bnbnode.accepted),len(bnbnode.rejected)))
    for edge in graph_edges:
        if((edge[0] in bnbnode.rejected)and(edge[1] in bnbnode.accepted)):
            LB+=int(edge[2].get('weight',1))
        elif ((edge[1] in bnbnode.rejected)and(edge[0] in bnbnode.accepted)):
             LB+=int(edge[2].get('weight',1))

   
    if(min(len(bnbnode.accepted),len(bnbnode.rejected))>0): return LB/(min(len(bnbnode.accepted),len(bnbnode.rejected)))
    return LB

 


        

