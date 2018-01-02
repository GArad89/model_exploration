from engine.baisc_entities.graph import DGraph
from engine.clustering import SpectralCluster
from engine.stopping_criteria.stopCriteria import SizeCriteria
from engine.baisc_entities.dendrogram import Node,Dendrogram
from engine.main.partitionLoop import partition

import os
from utils import project_root

def test_partition():
    den = None
    g = DGraph.read_dot(os.path.join(project_root(), "engine/dot/weighted_g2.dot"))
    print("testing partition on g2.dot for threshold=4:")
    den = partition(g, SpectralCluster.SpectralCluster(), SizeCriteria(4))

    assert len(den.node_list) == 3
    
    print("testing partition on g2.dot for threshold=2:")
    den = partition(g, SpectralCluster.SpectralCluster(), SizeCriteria(2))
    assert len(den.node_list) == 7
    
