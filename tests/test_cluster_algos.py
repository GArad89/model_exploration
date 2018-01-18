from .utils import test_init_seed
test_init_seed()

import unittest
from engine.clustering import SpectralCluster, minimum_cut, KMeans, BranchAndBound
from engine.basic_entities.graph import DGraph
from .utils import project_root
from os.path import join


def clusters_to_set(clusters):
    # as a set of sets, clusters can be compared by equality
    return {frozenset(cluster) for cluster in clusters}


class TestClusterAlgos(unittest.TestCase):

    def isEqualClusters(self, ideal_result, algo_result):
        algo_result.sort()
        for v in algo_result:
            v.sort()
        return (ideal_result == algo_result)

    def assertIsClusterRepresentation(self, algo_result, error_msg):
        assert isinstance(algo_result, list), error_msg
        for cluster in algo_result:
            assert isinstance(cluster,list), error_msg

    def test_branch_and_bound(self):
        print("Testing Branch and Bound")
        g2 = DGraph.read_dot(join(project_root(), "engine/dot/g2.dot"))
        algo_result = BranchAndBound.BranchAndBoundCluster().cluster(g2)
        self.assertIsClusterRepresentation(algo_result,"BnB result is not a lists of clusters when testing g2.dot")
        expected = clusters_to_set([['1', '2', '3', '4'], ['5', '6', '7']])
        assert clusters_to_set(algo_result) == expected, "BnB did not work as expected on g2.dot"

    def test_Kmeans(self):
        print("Testing Kmeans")
        g2 = DGraph.read_dot(join(project_root(), "engine/dot/g2.dot"))
        algo_result = KMeans.KMeansClustering().cluster(g2)
        self.assertIsClusterRepresentation(algo_result, "Kmeans result is not a lists of clusters when testing g2.dot")
        expected = clusters_to_set([['1', '2', '3', '4'], ['5', '6', '7']])
        assert clusters_to_set(algo_result) == expected, "Kmeans did not work as expected on g2.dot"

    def test_minimum_cut(self):
        print("Testing MinimumCut")
        g2 = DGraph.read_dot(join(project_root(), "engine/dot/g2.dot"))
        algo_result = minimum_cut.MinimumCut().cluster(g2)
        self.assertIsClusterRepresentation(algo_result, "MinimumCut result is not a lists of clusters when testing g2.dot")
        #To-Do minimum_cut further tests on different inputs

    def test_spectral(self):
        print("Testing Spectral Clustering")
        g2 = DGraph.read_dot(join(project_root(), "engine/dot/g2.dot"))
        algo_result = SpectralCluster.SpectralCluster().cluster(g2)
        self.assertIsClusterRepresentation(algo_result, "SpectralCluster result is not a lists of clusters when testing g2.dot")
        expected = clusters_to_set([['1', '2', '3', '4'], ['5', '6', '7']])
        assert clusters_to_set(algo_result) == expected, "SpectralCluster did not work as expected on g2.dot"


if __name__ == '__main__':
    unittest.main()
