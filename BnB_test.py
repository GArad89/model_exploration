from engine.clustering.Branch_and_Bound import *
from engine.baisc_entities.graph import DGraph
import networkx as nx
from engine.main.engineMainFlow import run_algo

# just a file to mess with the BnB Algo. not going to stay here for the final product##
g=DGraph.read_dot("./engine/dot/graph.dot")
BranchAndBoundCluster(sparset_cut_target,lower_bound_greedy_simple, upper_bound_greedy_simple, sort_nodes_by_degree).cluster(g, debug_print=True)
#print(run_algo(DGraph.read_dot("./engine/dot/weighted_g2.dot"),"SpectralCluster",None,stopCriteria="SizeCriteria"))
