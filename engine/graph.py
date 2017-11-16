import networkx as nx
import matplotlib.pyplot as plt
from random import *
from _functools import partial

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
    
    def edges_ofnode(self, node): #method currently isn't used.
        return self.dgraph.edges(node)

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

    def adjacency_matrix(self):
        return nx.to_numpy_matrix(self.dgraph)

    def subgraph(self, vertices):
        return self.dgraph.subgraph(vertices)  #subgraph is read only. probably a useless method

  

    @staticmethod
    def read_dot(path):
        return DGraph(nx.drawing.nx_pydot.read_dot(path))

    def project(self, vertices):   #, inNode, outNode
       # partialGraph = self.subgraph(vertices)
        projectedGraph=DGraph(nx.DiGraph()) #couldn't get DGraph(self) to work for some reason.
          
       # partialGraph.add_node("inNode") #gives error: SubGraph Views are readonly. Mutations not allowed

       #naive solution for now:
        for node in vertices:
           projectedGraph.add_node(node)
              
        projectedGraph.add_node("inNode")
        projectedGraph.add_node("outNode")

        for edge1,edge2 in list(self.edges()):
            if (edge1 in vertices):
                if (edge2 in vertices):
                    projectedGraph.add_edge(edge1,edge2)
                else:
                    projectedGraph.add_edge(edge1,"outNode")
            else:
                if(edge2 in vertices):
                    projectedGraph.add_edge("inNode",edge2)
        
        
        """   #previous code:
        for node in vertices:
            for edge in self.out_edges(node):
                if edge not in  projectedGraph.out_edges(node):
                     projectedGraph.add_edge(node,outNode)
            for edge in self.in_edges(node):
                if edge not in  projectedGraph.in_edges(node):
                     projectedGraph.add_edge(inNode,node)      
        """        

                    
        return projectedGraph
    

       
  
                    



# for testing purposes
def main():
    g = DGraph.read_dot("./dot/g2.dot")
    #g.draw()
   # new_node = random() * 10000
    #g.add_node(new_node)
    #DGraph.write_dot(g, "./dot/g2.dot")

def projectedgraph_test():
    g = DGraph.read_dot("./dot/g2.dot")
    print(g.project([1,2,3]).nodes())
    
if __name__ == "__main__":
   main()
   #projectedgraph_test()

