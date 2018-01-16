import unittest
from engine.baisc_entities.graph import *
from utils import *

class Test_DGraph(unittest.TestCase):

    def test_init(self):
        self.assertIsNotNone(DGraph(nx.DiGraph()),"DGraph init failed")
        
        
    def test_nodes(self):
        g=DGraph(nx.DiGraph())
        g.add_node('1' , label='kekek')
        g.add_node('2')
        g.add_node('3')
        g.add_node('4')

        self.assertEqual(len(g.nodes()),4, "wrong number of nodes ")
        self.assertEqual(set(g.nodes()),{'1', '2', '3', '4'}, "wrong set of nodes")

    def test_edges(self):
        g=DGraph(nx.DiGraph())
        g.add_node('1' , label='kekek')
        g.add_node('2')
        g.add_node('3')
        g.add_node('4')
        g.add_edge('1','2',weight=2)
        g.add_edge('3','2',weight=2)
        self.assertEqual(len(g.edges()),2, "wrong number of edges ")


class Test_GraphImporter(unittest.TestCase):

    def test_import_example(self):
        self.assertIsNotNone(DGraph.read_dot("./engine/dot/example.dot"),"import of example.dot failed")
        g=DGraph.read_dot("./engine/dot/example.dot")
        self.assertEqual(len(g.nodes()),24, "wrong number of nodes after import")
        
    def test_import_zip(self):
        self.assertIsNotNone(DGraph.read_dot("./engine/dot/zip.dot"),"import of zip.dot failed")
        g=DGraph.read_dot("./engine/dot/zip.dot")
        self.assertEqual(len(g.nodes()),5, "wrong number of nodes after import")
        self.assertEqual(len(g.edges()),9, "wrong number of edges after import")

class Test_GraphExporter(unittest.TestCase):

    def test_import_and_export(self):
        self.assertIsNotNone(DGraph.read_dot("./engine/dot/example.dot"),"import of example.dot failed")
        g=DGraph.read_dot("./engine/dot/example.dot")
        g.write_dot("./tests/dot_export/example.dot")
        self.assertIsNotNone(DGraph.read_dot("./tests/dot_export/example.dot"),"import of exported example.dot failed")
        g=DGraph.read_dot("./tests/dot_export/example.dot")
        self.assertEqual(len(g.nodes()),24, "wrong number of nodes after export")
        
    def test_builtgraph_export(self):
        g=DGraph(nx.DiGraph())
        g.add_node('1' , label='kekek')
        g.add_node('2')
        g.add_node('3')
        g.add_node('4')
        g.add_edge('1','2',weight=2)
        g.add_edge('3','2',weight=2)
        g.write_dot("./tests/dot_export/g.dot")
        self.assertIsNotNone(DGraph.read_dot("./tests/dot_export/g.dot"),"import of exported g.dot failed")
        g=DGraph.read_dot("./tests/dot_export/g.dot")
        self.assertEqual(len(g.nodes()),4, "wrong number of nodes after export")
        self.assertEqual(len(g.edges()),2, "wrong number of edges after export")



if __name__ == '__main__':
    unittest.main()
