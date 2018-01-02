from engine.clustering.KernighanLinCluster import KernighanLinCluster
from engine.baisc_entities.graph import DGraph
from engine.main.partitionLoop import partition
from engine.stopping_criteria.stopCriteria import SizeCriteria
import unittest


class Test_KL(unittest.TestCase):

    def test_kerningham_lin(self):
        g = DGraph.read_dot("../engine/dot/cvs.net.mutated.dot")
        KL = KernighanLinCluster()
        dendrogram = partition(g, clustering_algo=KL, stopCri=SizeCriteria(3))
        print("foo")


if __name__ == '__main__':
    unittest.main()

