from graph import DGraph

class Cluster:
    parent = None
    label = None
    children_clusters = []
    subset = []
    projected_graph = None
    
    def __init__(self, parent = None, subset = [],dgraph = None,label = None):
        if (parent == None):
            if (label == None):
                self.label = 'root'
        else:
            self.parent = parent
            self.label = label

        self.subset = subset
        self.projected_graph = dgraph
        self.children_clusters = []

    def add_child(self, cluster_child):
        self.children_clusters += [cluster_child]

    def parent(self):
        return self.parent

    def children(self):
        return self.children_clusters

    def get_label(self):
        return self.label

    def vertices(self):
        return self.subset

    def set(self, subset, projected_graph):
        self.subset = subset
        self.projected_graph = projected_graph
        
    
class Dendrogram:
    dgraph = None
    root_cluster = None
    number_of_clusters = 0

    def __init__(self,dgraph):
        self.root_cluster = Cluster(None,dgraph.nodes()) #root cluster
        self.dgraph=dgraph
        self.number_of_clusters = 1

    def add_cluster(self, cluster, parent):
        parent.add_child(cluster)
        self.number_of_clusters += 1

    def root(self):
        return self.root_cluster

    def label_by_order(self, node):
        node.label = 'Node ' + str(self.number_of_clusters)

    def label_by_sum_names(self, node):
        label_temp = ''
        # label_list=
        # print(label_list)
        for graph_node in node.projected_graph.dgraph.nodes():
            temp = str(node.projected_graph.dgraph.node[graph_node]['label'])
            if (temp != 'None'):
                label_temp += temp
        if (label_temp != ''):
            node.label = label_temp
        else:
            self.label_by_order(node)






