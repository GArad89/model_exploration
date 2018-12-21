from engine.clustering.KernighanLinCluster import KernighanLinCluster
from engine.basic_entities.graph import DGraph
from engine.main.partition import partition
from engine.stopping_criteria.stop_criteria import SizeCriteria
import unittest

import os
from .utils import project_root

class Test_KL(unittest.TestCase):

    def test_kerningham_lin(self):
        g = DGraph.read_dot(os.path.join(project_root(), "dot/cvs.net.mutated.dot"))
        KL = KernighanLinCluster()
        dendrogram = partition(g, clustering_algo=KL, stop_criterion=SizeCriteria(3))
        print("foo")


if __name__ == '__main__':
    unittest.main()

