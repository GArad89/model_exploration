import unittest
from engine.basic_entities.graph import DGraph
from engine.labeling import PageRankLabeler, label
from engine.clustering import SpectralCluster
from engine.main import engineMainFlow, partitionLoop
from engine.stopping_criteria import stopCriteria
from utils import project_root
from os.path import join

class RandomWalkLabelerTest(unittest.TestCase):

    def test_labeling(self):

        g = DGraph.read_dot(join(project_root(), "engine/dot/cvs.net.dot"))
        den = partitionLoop.partition(g, SpectralCluster.SpectralCluster(), stopCriteria.SizeCriteria(4))
        labeler = PageRankLabeler.PageRankLabeler(g, den, label.labeling_on_type.EDGES)
        labeler.label()

def main():
    unittest.main()
    
if __name__=='__main__':
    main()
