from engine.clustering.Branch_and_Bound import *
from engine.baisc_entities.graph import DGraph
import networkx as nx
from engine.main.engineMainFlow import run_algo

# just a file to mess with the BnB Algo. not going to stay here for the final product##
g=DGraph.read_dot("./engine/dot/weighted_g2.dot")
BranchAndBoundCluster.cluster(1,g,Sparset_Cut_Target,LB_Greedy_Simple, None, Sort_Nodes_byDegree)
#print(run_algo(DGraph.read_dot("./engine/dot/weighted_g2.dot"),"SpectralCluster",None,stopCriteria="SizeCriteria"))
