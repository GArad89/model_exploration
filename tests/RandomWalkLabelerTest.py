import unittest
from engine.basic_entities.graph import *
from engine.labeling import RandomWalkLabeler
from engine.clustering import SpectralCluster
from engine.main import engineMainFlow, partitionLoop
from engine.stopping_criteria import stopCriteria


class RandomWalkLabelerTest(unittest.TestCase):

    def test_labeling(self):
        import os
        cwd = os.getcwd()
        print(cwd)

        g = DGraph.read_dot("../engine/dot/java.util.Formatter.dot")
        den = partitionLoop.partition(g, SpectralCluster.SpectralCluster(), stopCriteria.SizeCriteria(4))
        labeler = RandomWalkLabeler.RandomWalkLabeler(g, den)
        labeler.label()
