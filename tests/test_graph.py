import unittest
from engine.basic_entities.graph import DGraph
from .utils import project_root
from os.path import join
import networkx as nx

class Test_DGraph(unittest.TestCase):

    def test_init(self):
        self.assertIsNotNone(DGraph().dgraph,"DGraph init failed")
        
    def test_nodes(self):
        g=DGraph()
        g.add_node('1' , label='kekek')
        g.add_node('2')
        g.add_node('3')
        g.add_node('4')

        self.assertEqual(len(g.nodes()),4, "wrong number of nodes ")
        self.assertEqual(set(g.nodes()),{'1', '2', '3', '4'}, "wrong set of nodes")

    def test_edges(self):
        g=DGraph()
        g.add_node('1' , label='kekek')
        g.add_node('2')
        g.add_node('3')
        g.add_node('4')
        g.add_edge('1','2',weight=2)
        g.add_edge('3','2',weight=2)
        self.assertEqual(len(g.edges()),2, "wrong number of edges ")


class Test_GraphImporter(unittest.TestCase):

    def test_import_example(self):
        g = DGraph.read_dot(join(project_root(), "./engine/dot/example.dot"))
        self.assertIsNotNone(g.dgraph, "import of example.dot failed")
        self.assertEqual(len(g.nodes()),24, "wrong number of nodes after import")
        
    def test_import_zip(self):
        g = DGraph.read_dot(join(project_root(), "./engine/dot/zip.dot"))
        self.assertIsNotNone(g.dgraph, "import of zip.dot failed")
        self.assertEqual(len(g.nodes()),5, "wrong number of nodes after import")
        self.assertEqual(len(g.edges()),9, "wrong number of edges after import")

class Test_GraphExporter(unittest.TestCase):

    def test_import_and_export(self):
        g = DGraph.read_dot(join(project_root(), "./engine/dot/example.dot"))
        self.assertIsNotNone(g,"import of example.dot failed")
        g.write_dot(join(project_root(), "./tests/dot_export/example.dot"))
        g2 = DGraph.read_dot(join(project_root(), "./tests/dot_export/example.dot"))
        self.assertIsNotNone(g2,"import of exported example.dot failed")
        self.assertEqual(len(g2.nodes()),24, "wrong number of nodes after export")
        assert nx.algorithms.is_isomorphic(g.dgraph, g2.dgraph)

    def test_builtgraph_export(self):
        g=DGraph()
        g.add_node('1' , label='kekek')
        g.add_node('2')
        g.add_node('3')
        g.add_node('4')
        g.add_edge('1','2',weight=2)
        g.add_edge('3','2',weight=2)
        g.write_dot(join(project_root(), "./tests/dot_export/g.dot"))
        g2 = DGraph.read_dot(join(project_root(), "./tests/dot_export/g.dot"))
        assert g2.dgraph is not None
        self.assertEqual(len(g.nodes()),4, "wrong number of nodes after export")
        self.assertEqual(len(g.edges()),2, "wrong number of edges after export")
        assert nx.algorithms.is_isomorphic(g.dgraph, g2.dgraph)



if __name__ == '__main__':
    unittest.main()
