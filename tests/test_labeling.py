import unittest
from engine.baisc_entities.graph import *
from engine.labeling import TfIdfLabeler
from engine.clustering import SpectralCluster
from engine.main import engineMainFlow, partitionLoop
from engine.stopping_criteria import stopCriteria

class Test_DGraph(unittest.TestCase):

    def test_labeling(self):
        g = DGraph.read_dot("engine/dot/ssh.net.dot")
        den = partitionLoop.partition(g, g.nodes(), SpectralCluster.SpectralCluster, stopCriteria.SizeCriteria(4))
        labeler = TfIdfLabeler.TfIdfLabeler(g, den)
        labeler.label()
