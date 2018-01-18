import networkx as nx
from itertools import chain
from numpy import zeros
from collections import OrderedDict

class OrderedDiGraph(nx.DiGraph):
    """
    nx.DiGraph that retains ordering when iterating on it
    """
    adjlist_outer_dict_factory = OrderedDict
    adjlist_inner_dict_factory = OrderedDict
    node_dict_factory = OrderedDict

class OrderedGraph(nx.DiGraph):
    """
    nx.DiGraph that retains ordering when iterating on it
    """
    adjlist_outer_dict_factory = OrderedDict
    adjlist_inner_dict_factory = OrderedDict
    node_dict_factory = OrderedDict


class DGraph:
    def __init__(self, nx_graph=None):
        self.dgraph = OrderedDiGraph() if nx_graph is None else nx_graph

    def add_node(self, node, label=None, **attr):
        self.dgraph.add_node(node,label=label, attr = attr)

    def add_edge(self, node1, node2, weight=None):
        if(weight == None):
            self.dgraph.add_edge(node1, node2)
        else:
            self.dgraph.add_edge(node1, node2, weight=weight)

    def nodes(self):
        return self.dgraph.nodes()

    def get_edge_data(self, edge):
        return self.dgraph.get_edge_data(edge[0], edge[1])

    def edges(self, data=True):
        return self.dgraph.edges(data=data)
    
    def edges_of_node(self, node): 
        return self.dgraph.edges(node)

    def in_edges(self, node):
        return self.dgraph.in_edges(node)

    def draw(self):
        import matplotlib.pyplot as plt
        nx.draw(self.dgraph)
        plt.show()

    def number_of_nodes(self):
        return self.dgraph.number_of_nodes()
    
    def number_of_edges(self):
        return self.dgraph.size()


    def node_attr(self, node, attr):
        return self.dgraph.nodes[node][attr]

    def write_dot(self, path):
        print("write_dot called")
        nx.drawing.nx_pydot.write_dot(self.dgraph, path)

    def adjacency_matrix(self, node_list=None):
        # order nodes' row,column according to list or according to dgraph.nodes() order
        if node_list is None:
            node_list = self.nodes()

        adj_mat = zeros(shape=(len(self.nodes()),len(self.nodes())))
        i = 0
        node_dict = {node : i for i, node in enumerate(node_list)}
            
        for edge in self.edges():
            adj_mat[node_dict[edge[0]]][node_dict[edge[1]]] += int(edge[2].get('weight',1))

        return adj_mat

    def subgraph(self, vertices):
        return self.dgraph.subgraph(vertices)  


    def maxInOutDegree(self):
        maxdeg = 0
        for node in self.dgraph.nodes():
            maxdeg = max(maxdeg,max(self.dgraph.in_degree(node), self.dgraph.out_degree(node)))
        return maxdeg

    def numberOfComponenets(self):
        return sum(1 for _ in nx.strongly_connected_components(self.dgraph))

    @staticmethod
    def read_dot(path):
        multigraph = nx.drawing.nx_pydot.read_dot(path)
        nx_graph = OrderedDiGraph()
        # create the graph ordered, for consistency when running algorithms
        for node, data in sorted(multigraph.nodes(data=True)):
            nx_graph.add_node(node, **data)

        for src, dst, data in multigraph.edges(data=True):
            nx_graph.add_edge(src, dst, **data)

        # deal with ""-encapsulated strings in properties
        # e.g. java.net.DatagramSocket.dot
        for item, attrs in chain(nx_graph.nodes.items(), nx_graph.edges.items()):
            for key in ('label', 'style'):
                if key in attrs:
                    # remove surrounding double-quotes
                    attrs[key] = attrs[key].strip().strip('"').strip()

        return DGraph(nx_graph)

    def project(self, vertices):  
        return DGraph(self.subgraph(vertices))     

# for testing purposes
def main():
    g = DGraph.read_dot("./dot/example.dot")
    #for n in g.dgraph.nodes():
        #print(g.dgraph.node[n]['label'])
    g.draw() 
    #new_node = random() * 10000 
    #g.add_node(new_node, weight=0.4)
    #g.add_edge(2, '1', weight=0.2)
    #DGraph.write_dot(g, "./dot/g1.dot") 
 


def projectedgraph_test():
    #g = DGraph.read_dot("./dot/weighted_g2.dot")
    g=DGraph(nx.DiGraph())
    g.add_node('1' , label='kekek')
    g.add_node('2')
    g.add_node('3')
    g.add_node('4')
    g.add_edge('1','2',weight=2)
    g.add_edge('3','2',weight=2)
    #print(list(g.edges_of_node('3'))[0][0])
    #DGraph.write_dot(g, "./dot/test.dot")
    
    
if __name__ == "__main__":
   #main()
   projectedgraph_test()

