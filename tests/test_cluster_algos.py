import unittest
from engine.clustering import SpectralCluster, minimum_cut, Kmeans, Branch_and_Bound
from engine.baisc_entities.graph import DGraph


class TestClusterAlgos(unittest.TestCase):

    def isEqualClusters(self, ideal_result, algo_result):
        algo_result.sort()
        for v in algo_result:
            v.sort
        return (ideal_result == algo_result)

    def assertIsClusterRepresentation(self, algo_result, error_msg):
        self.assertTrue(isinstance(algo_result, list), error_msg)
        for cluster in algo_result:
            self.assertTrue(isinstance(cluster,list),error_msg)

    def test_Branch_and_Bound(self):
        print("Testing Branch and Bound")
        g2 = DGraph.read_dot("./engine/dot/g2.dot")
        algo_result = Branch_and_Bound.BranchAndBoundCluster.cluster(1, g2,None,None,None,None)
        self.assertIsClusterRepresentation(algo_result,"BnB result is not a lists of clusters when testing g2.dot")
        self.assertTrue(self.isEqualClusters([['1', '2', '3'], ['4', '5', '6', '7']], algo_result),"BnB did not work as expected on g2.dot")

    def test_Kmeans(self):
        print("Testing Kmeans")
        g2 = DGraph.read_dot("./engine/dot/g2.dot")
        algo_result = Kmeans.KmeansClustering.cluster(g2)
        self.assertIsClusterRepresentation(algo_result, "Kmeans result is not a lists of clusters when testing g2.dot")
        self.assertTrue(self.isEqualClusters([['1', '2', '3'], ['4', '5', '6', '7']], algo_result),"Kmeans did not work as expected on g2.dot")

    def test_minimum_cut(self):
        print("Testing MinimumCut")
        g2 = DGraph.read_dot("./engine/dot/g2.dot")
        algo_result = minimum_cut.MinimumCut.cluster(g2)
        self.assertIsClusterRepresentation(algo_result, "MinimumCut result is not a lists of clusters when testing g2.dot")
        #To-Do minimum_cut further tests on different inputs

    def test_spectral(self):
        print("Testing Spectral Clustering")
        g2 = DGraph.read_dot("./engine/dot/g2.dot")
        algo_result = SpectralCluster.SpectralCluster.cluster(g2)
        self.assertIsClusterRepresentation(algo_result, "SpectralCluster result is not a lists of clusters when testing g2.dot")
        ideal_1_bool = self.isEqualClusters([['1', '2', '3'], ['4', '5', '6', '7']], algo_result)
        ideal_2_bool = self.isEqualClusters([['1', '2', '3','4'], ['5', '6', '7']], algo_result)
        self.assertTrue((ideal_1_bool | ideal_2_bool),"SpectralCluster did not work as expected on g2.dot")


if __name__ == '__main__':
    unittest.main()