import unittest
from engine.baisc_entities.graph import *
from engine.labeling import PageRankLabeler
from engine.clustering import SpectralCluster
from engine.main import engineMainFlow, partitionLoop
from engine.stopping_criteria import stopCriteria


class RandomWalkLabelerTest(unittest.TestCase):

    def test_labeling(self):
        import os
        cwd = os.getcwd()
        print(cwd)

        g = DGraph.read_dot("../engine/dot/large/ktails3.dot")
        den = partitionLoop.partition(g, SpectralCluster.SpectralCluster(), stopCriteria.SizeCriteria(4))
        labeler = PageRankLabeler.PageRankLabeler(g, den)
        labeler.label()
