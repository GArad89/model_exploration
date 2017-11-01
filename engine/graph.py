import networkx as nx
import matplotlib.pyplot as plt
from random import *

class DGraph:
    dgraph = None
    def __init__(self):
        self.dgraph = nx.DiGraph()

    def __init__(self, nx_graph):
        self.dgraph = nx_graph

    def add_node(self, node, **attr):
        self.dgraph.add_node(node, attr = attr)

    def add_edge(self, node1, node2):
        self.dgraph.add_edge(node1, node2)

    def nodes(self):
        return self.dgraph.nodes()

    def edges(self):
        return self.dgraph.edges()

    def draw(self):
        nx.draw(self.dgraph)
        plt.show()

    def number_of_nodes(self):
        return self.dgraph.number_of_nodes()

    def node_attr(self, node, attr):
        return self.dgraph.nodes[node]['attr'][attr]

    def write_dot(self, path):
        print("write_dot called")
        nx.drawing.nx_pydot.write_dot(self.dgraph, path)

    @staticmethod
    def read_dot(path):
        return DGraph(nx.drawing.nx_pydot.read_dot(path))

    def project(vertices):
        pass

# for testing purposes
def main():
    g = DGraph.read_dot("./dot/g1.dot")
    g.draw()
    new_node = random() * 10000
    g.add_node(new_node)
    DGraph.write_dot(g, "./dot/g1.dot")


if __name__ == "__main__":
   main()
