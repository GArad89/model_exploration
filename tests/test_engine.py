import unittest
from engine.clustering import SpectralCluster, minimum_cut, Kmeans, Branch_and_Bound
from engine.baisc_entities.graph import DGraph
from engine.main import engineMainFlow, partitionLoop
from engine.stopping_criteria import stopCriteria

class TestEngine(unittest.TestCase):
    def test_partition(self):
        den = None
        g = DGraph.read_dot("./engine/dot/g2.dot")
        # den=partition(g,g.nodes())
        # print(len(den.node_list))  #should be 1 (root node only)
        print("testing partition on g2.dot for threshold=4")
        den = partitionLoop.partition(g, g.nodes(), SpectralCluster.SpectralCluster, stopCriteria.SizeCriteria(4))
        self.assertEqual(len(den.node_list), 3, "Expected number super-nodes in the dendogram (including the root) is 3")

        print("testing partition on g2.dot for threshold=2")
        den = partitionLoop.partition(g, g.nodes(), SpectralCluster.SpectralCluster, stopCriteria.SizeCriteria(2), dendrogram=None)
        self.assertEqual(len(den.node_list), 7, "Expected number super-nodes in the dendogram (including the root) is 7")


if __name__ == '__main__':
    unittest.main()
