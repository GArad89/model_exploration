import unittest
from engine.basic_entities.graph import DGraph
from engine.labeling import PageRankLabeler, label
from engine.clustering import SpectralCluster
from engine.main import partition
from engine.stopping_criteria import stop_criteria
from .utils import project_root
from os.path import join

class RandomWalkLabelerTest(unittest.TestCase):

    def test_labeling(self):

        g = DGraph.read_dot(join(project_root(), "dot/cvs.net.dot"))
        den = partition.partition(g, SpectralCluster.SpectralCluster(), stop_criteria.SizeCriteria(4))
        labeler = PageRankLabeler.PageRankLabeler(g, den, label.labeling_on_type.EDGES)
        labeler.label()

def main():
    unittest.main()
    
if __name__=='__main__':
    main()
