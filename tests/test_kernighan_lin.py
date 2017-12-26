import sys
sys.path.append('..')
from networkx.classes import graph
from engine.clustering.minimum_cut import MinimumCut
from engine.clustering.KernighanLinCluster import KernighanLinCluster
from engine.baisc_entities.graph import DGraph
from engine.main.partitionLoop import partition
from engine.stopping_criteria.stopCriteria import SizeCriteria

def test_kerningham_lin():
    den = None
    g = DGraph.read_dot("engine/dot/cvs.net.mutated.dot")
    mc = MinimumCut()
    res = mc.cluster(g)

    partition(g, clustering_algo = KernighanLinCluster, stopCri = SizeCriteria(3))

