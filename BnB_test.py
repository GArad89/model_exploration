from engine.clustering.Branch_and_Bound import *
from engine.baisc_entities.graph import DGraph
import networkx as nx

g=DGraph.read_dot("./engine/dot/g2.dot")
BranchAndBoundCluster.cluster(1,g,Sparset_Cut_Target,LB_Greedy_Simple, None, Sort_Nodes)
