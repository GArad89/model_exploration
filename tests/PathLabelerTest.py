import unittest
from engine.baisc_entities.graph import *
from engine.labeling import PathLabeler
from engine.clustering import SpectralCluster
from engine.main import engineMainFlow, partitionLoop
from engine.stopping_criteria import stopCriteria


class PathLabelerTest(unittest.TestCase):

    def test_labeling(self):

        g = DGraph.read_dot("../engine/dot/large/ktails4.dot")
        den = partitionLoop.partition(g, SpectralCluster.SpectralCluster(), stopCriteria.SizeCriteria(4))
        labeler = PathLabeler.PathLabeler(g, den, None)
        labeler.label()
