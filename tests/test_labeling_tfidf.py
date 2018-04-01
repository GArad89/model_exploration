import unittest
from engine.basic_entities.graph import DGraph
from engine.labeling import TfIdfLabeler
from engine.clustering import SpectralCluster
from engine.main import partition
from engine.stopping_criteria import stop_criteria

import os
from .utils import project_root

class Test_DGraph(unittest.TestCase):

    def test_labeling(self):
        g = DGraph.read_dot(os.path.join(project_root(), "dot/ssh.net.dot"))
        den = partition.partition(g, SpectralCluster.SpectralCluster(), stop_criteria.SizeCriteria(4))
        labeler = TfIdfLabeler.TfIdfLabeler(g, den, 'Both')
        labeler.label()
