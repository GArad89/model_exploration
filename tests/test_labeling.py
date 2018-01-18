import unittest
from engine.basic_entities.graph import DGraph
from engine.labeling import TfIdfLabeler
from engine.clustering import SpectralCluster
from engine.main import engineMainFlow, partitionLoop
from engine.stopping_criteria import stopCriteria

import os
from .utils import project_root

class Test_DGraph(unittest.TestCase):

    def test_labeling(self):
        g = DGraph.read_dot(os.path.join(project_root(), "engine/dot/ssh.net.dot"))
        den = partitionLoop.partition(g, SpectralCluster.SpectralCluster(), stopCriteria.SizeCriteria(4))
        labeler = TfIdfLabeler.TfIdfLabeler(g, den, 'Both')
        labeler.label()
