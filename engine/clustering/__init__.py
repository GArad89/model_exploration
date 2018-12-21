from . import KMeans, SpectralCluster, minimum_cut, BranchAndBound, KernighanLinCluster

def get_algorithms():
    "return list of clustering classes"
    return [KMeans.KMeansClustering, SpectralCluster.SpectralCluster, minimum_cut.MinimumCut, 
            BranchAndBound.BranchAndBoundCluster, KernighanLinCluster.KernighanLinCluster]

def get_cluster_algorithm(algorithm_name):
    "return class for specific algorithm"
    algorithms = get_algorithms()
    return algorithms[[algo.__name__ for algo in algorithms].index(algorithm_name)]