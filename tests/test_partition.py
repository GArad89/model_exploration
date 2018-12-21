from .utils import test_init_seed
test_init_seed()

from engine.basic_entities.graph import DGraph
from engine.clustering import SpectralCluster
from engine.stopping_criteria.stop_criteria import SizeCriteria
from engine.main.partition import partition

import os
from .utils import project_root

def test_partition():
    den = None
    g = DGraph.read_dot(os.path.join(project_root(), "dot/weighted_g2.dot"))
    print("testing partition on g2.dot for threshold=4:")
    den = partition(g, SpectralCluster.SpectralCluster(), SizeCriteria(4))
    assert len(den.node_list) == 10
    
    print("testing partition on g2.dot for threshold=2:")
    den = partition(g, SpectralCluster.SpectralCluster(), SizeCriteria(2))
    print('expected:', len(den.node_list))
    assert len(den.node_list) == 13


