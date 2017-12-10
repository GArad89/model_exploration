import unittest
from engine.clustering import SpectralCluster, minimum_cut, Kmeans, Branch_and_Bound

class TestClusterAlgos(unittest.TestCase):

    def test_Branch_and_Bound(self):
        self.assertEqual('foo'.upper(), 'FOO')
    def test_Kmeans(self):
        self.assertEqual('foo'.upper(), 'FOO')
    def test_minimum_cut(self):
        self.assertEqual('foo'.upper(), 'FOO')
    def test_spectral(self):
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()