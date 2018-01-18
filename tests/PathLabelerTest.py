import unittest
from engine.basic_entities.graph import *
from engine.labeling import PathLabeler
from engine.clustering import SpectralCluster
from engine.main import engineMainFlow, partitionLoop
from engine.stopping_criteria import stopCriteria
from .utils import project_root
from os.path import join


class PathLabelerTest(unittest.TestCase):

    def test_labeling(self):

        g = DGraph.read_dot(join(project_root(), "engine/dot/large/ktails4.dot"))
        den = partitionLoop.partition(g, SpectralCluster.SpectralCluster(), stopCriteria.SizeCriteria(4))
        labeler = PathLabeler.PathLabeler(g, den, None)
        labeler.label()
