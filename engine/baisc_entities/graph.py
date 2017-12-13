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

    def add_node(self, node, label=None, **attr):
        self.dgraph.add_node(node,label=label, attr = attr)

    def add_edge(self, node1, node2, weight=None):
        if(weight == None):
            self.dgraph.add_edge(node1, node2)
        else:
            self.dgraph.add_edge(node1, node2, weight=weight)

    def nodes(self):
        return self.dgraph.nodes()

    def edges(self, data=None):
        return self.dgraph.edges(data=data)
    
    def edges_of_node(self, node): 
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
        return DGraph(nx.DiGraph(nx.drawing.nx_pydot.read_dot(path)))

    def project(self, vertices):   #, inNode, outNode
       # partialGraph = self.subgraph(vertices)
        projectedGraph=DGraph(nx.DiGraph()) #couldn't get DGraph(self) to work for some reason.
          
       # partialGraph.add_node("inNode") #gives error: SubGraph Views are readonly. Mutations not allowed

       #naive solution for now:
        for node in vertices:
           if(node!="inNode")and(node!="outNode"): 
               temp=self.dgraph.node[node].get('label',None)
               if(temp!=None):
                   projectedGraph.add_node(node,label=self.dgraph.node[node]['label'])
               else:
                   projectedGraph.add_node(node)
       
        projectedGraph.add_node("inNode")
        projectedGraph.add_node("outNode")

        for edge1,edge2,dic in list(self.dgraph.edges(data=True)):
            weight=dic.get('weight', 1)
            
            if (edge1 in vertices):
                if (edge2 in vertices):
                    projectedGraph.add_edge(edge1, edge2, weight)
                else:
                    projectedGraph.add_edge(edge1, "outNode", weight)
            else:
                if(edge2 in vertices):
                    projectedGraph.add_edge("inNode", edge2, weight)
        
        
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
    g = DGraph.read_dot("./dot/example.dot")
    #for n in g.dgraph.nodes():
        #print(g.dgraph.node[n]['label'])
    g.draw() 
    new_node = random() * 10000 
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

