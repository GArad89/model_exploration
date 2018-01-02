from . import Kmeans, SpectralCluster, minimum_cut, Branch_and_Bound, KernighanLinCluster

def get_algorithms():
    "return list of clustering classes"
    return [Kmeans.KmeansClustering, SpectralCluster.SpectralCluster, minimum_cut.MinimumCut, 
            Branch_and_Bound.BranchAndBoundCluster, KernighanLinCluster.KernighanLinCluster]

def get_cluster_algorithm(algorithm_name):
    "return class for specific algorithm"
    algorithms = get_algorithms()
    return algorithms[[algo.__name__ for algo in algorithms].index(algorithm_name)]