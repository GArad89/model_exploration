import unittest
from engine.basic_entities.graph import DGraph
from engine.labeling import PathLabeler
from engine.clustering import SpectralCluster
from engine.main import partition
from engine.stopping_criteria import stop_criteria
from .utils import project_root
from os.path import join
from engine.labeling import labeling_on_type


class PathLabelerTest(unittest.TestCase):

    def test_labeling(self):

        g = DGraph.read_dot(join(project_root(), "engine/dot/large/ktails4.dot"))
        den = partition.partition(g, SpectralCluster.SpectralCluster(), stop_criteria.SizeCriteria(4))
        labeler = PathLabeler.PathLabeler(g, den, labeling_on_type.EDGES)
        labeler.label()
