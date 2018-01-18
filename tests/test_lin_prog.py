from utils import test_init_seed
test_init_seed()

from engine.linear_programming.lin_prog_solver import LPS
from engine.utils.NxGraphUtil import draw
from engine.utils.NxGraphUtil import write_nx_graph_to_file
from engine.utils.FileWriter import log
from engine.utils.IOUtils import delete_files_from_folder
from engine.basic_entities.graph import OrderedGraph

import networkx as nx
from random import randint
import unittest
import os

class LPTest(unittest.TestCase):
    OUT_FOLDER = os.path.join(os.path.dirname(__file__),'../results/linear_programming/')
    GRAPH_PLOTS_PATH = OUT_FOLDER + 'plots/'
    GRAPH_DOT_PATH = OUT_FOLDER + 'dot/'
    CLICKS_EXPERIMENT_LOG_PATH = OUT_FOLDER + 'click_graph_results.txt'
    CLICKS_EXPERIMENT_WITH_PARTIAL_LOG_PATH = OUT_FOLDER + 'click_graph_partial_results.txt'
    RANDOM_EXPERIMENT_LOG_PATH = OUT_FOLDER + 'random_graph_results.txt'
    TOY_EXPERIMENT_LOG_PATH = OUT_FOLDER + 'toy_graph_results.txt'
    TOY_PARTIAL_ASSIGNMENT_EXPERIMENT_LOG_PATH = OUT_FOLDER + 'parital_assignment_graph_results.txt'
    CLICKS_SIZE = 10
    RANDOM_GRAPH_NODES = 10
    RANDOM_GRAPH_EDGES = 20
    RANDOM_GRAPH_MIN_WEIGHT = 10
    RANDOM_GRAPH_MAX_WEIGHT = 10

    @staticmethod
    def _generate_two_connected_clicks_example(n):

        G = OrderedGraph()
        for i in range(n):
            G.add_node(i)

        for i in range(int(n / 2)):
            for j in range(int(n / 2)):
                if i == j:
                    continue
                G.add_edge(i, j, weight=5)
                G.add_edge(j, i, weight=5)

        for i in range(int(n / 2), n):
            for j in range(int(n / 2), n):
                if i == j:
                    continue
                G.add_edge(i, j, weight=5)
                G.add_edge(j, i, weight=5)

        G.add_edge(0, n - 1, weight=5)
        G.add_edge(n - 1, 0, weight=5)
        G.add_edge(1, n - 2, weight=5)
        G.add_edge(n - 2, 1, weight=5)

        if LPTest.GRAPH_PLOTS_PATH:
            draw(G, LPTest.GRAPH_PLOTS_PATH + "click_graph.png")
        if LPTest.GRAPH_DOT_PATH:
            write_nx_graph_to_file(G, LPTest.GRAPH_DOT_PATH + "click_graph.dot")

        return G

    @staticmethod
    def _generate_toy_example():

        G = OrderedGraph()
        a = "A"
        for i in range(5):
            G.add_node(i, label=a, attr=a)
            a = chr(ord('c') + 1)

        for i in range(0, 3):
            G.add_edge(0, i, weight=2)

        G.add_edge(1, 2, weight=4)
        G.add_edge(3, 4, weight=4)
        G.add_edge(3, 2, weight=6)

        if LPTest.GRAPH_PLOTS_PATH:
            draw(G, LPTest.GRAPH_PLOTS_PATH + "toy_graph.png")
        if LPTest.GRAPH_DOT_PATH:
            write_nx_graph_to_file(G, LPTest.GRAPH_DOT_PATH + "toy_graph.dot")

        return G

    @staticmethod
    def _generate_random_graph(total_nodes, total_edges, min_weight=0, max_weight=1):

        G = OrderedGraph()
        for i in range(total_nodes):
            G.add_node(i)

        edges = set()
        if total_edges < total_nodes - 1:
            raise ValueError('#nodes > #edges, cannot generate at least one edge per node')
        for i in range(total_nodes):
            j = 0
            while j == i:
                j = randint(0, total_nodes)
            w = randint(min_weight, max_weight)
            G.add_edge(i, j, weight=w)
            edges.add((i, j))

        while len(edges) < total_edges:
            j = randint(0, total_nodes)
            k = randint(0, total_nodes)
            if j == k:
                continue
            if (j, k) not in edges:
                edges.add((j, k))
                w = randint(min_weight, max_weight)
                G.add_edge(j, k, weight=w)

        if LPTest.GRAPH_PLOTS_PATH:
            draw(G, LPTest.GRAPH_PLOTS_PATH + 'random_graph.png')
        if LPTest.GRAPH_DOT_PATH:
            write_nx_graph_to_file(G, LPTest.GRAPH_DOT_PATH + "random_graph.dot")

        return G

    @staticmethod
    def _run_experiment(G, log_path, partial_assignment_dict={}):

        lps = LPS()
        lower, cut, value = lps.solve(G, partial_assignment_dict, log_path)
        msg = "lower bound: " + str(lower) + "\n"
        msg += "best cut " + str(cut) + ":  " + str(value)
        log(msg, log_path)
        return lower, cut, value

    def setUp(self):
        delete_files_from_folder(self.GRAPH_DOT_PATH)
        delete_files_from_folder(self.GRAPH_PLOTS_PATH)
        delete_files_from_folder(self.OUT_FOLDER)

    def test_toy(self):

        G = self._generate_toy_example()
        lower, cut, value = self._run_experiment(G, self.TOY_EXPERIMENT_LOG_PATH)
        assert lower == 2.5
        assert 3.0 <= value <= 4.0
        assert len(cut) >= 1

    def test_toy_with_partial_assignment_test(self):

        G = self._generate_toy_example()
        partial_assignment_dict = {0: 0, 3: 1, 4: 0}  # None #{0: 0, 3: 1, 4: 0}
        lower, cut, value = self._run_experiment(G, self.TOY_PARTIAL_ASSIGNMENT_EXPERIMENT_LOG_PATH, partial_assignment_dict)
        assert abs(lower - 4.66666666667) < 0.001
        assert value == 4.0
        assert len(cut) > 0

    # def test_two_connected_clicks_test(self):
    #
    #     G = self._generate_two_connected_clicks_example(self.CLICKS_SIZE)
    #     lower, cut, value = self._run_experiment(G, self.CLICKS_EXPERIMENT_LOG_PATH)
    #     self.assertEqual(abs(lower-4.0) < 0.001, True)
    #     self.assertEqual(value == 4.0, True)
    #     self.assertEqual(cut == ['5', '6', '7', '8', '9'], True)

    # def test_two_connected_clicks_test_with_partial(self):
    #
    #     G = self._generate_two_connected_clicks_example(self.CLICKS_SIZE)
    #     partial_assignment_dict = {0: 0, 9: 0, 8: 1}
    #     lower, cut, value = self._run_experiment(G, self.CLICKS_EXPERIMENT_WITH_PARTIAL_LOG_PATH,
    #                                              partial_assignment_dict)
    #     self.assertEqual(lower == 11.0, True)
    #     self.assertEqual(value == 12.5, True)
    #     self.assertEqual(cut == ['0', '9', '1', '2', '3', '4'], True)
    #
    # def test_auto_generated_graph(self):
    #
    #     G = self._generate_random_graph(self.RANDOM_GRAPH_NODES, self.RANDOM_GRAPH_EDGES,
    #                                     self.RANDOM_GRAPH_MIN_WEIGHT, self.RANDOM_GRAPH_MAX_WEIGHT)
    #     weights = nx.get_edge_attributes(G, 'weight')
    #     total_weight = sum(weights.values())
    #     lower, cut, value = self._run_experiment(G, self.RANDOM_EXPERIMENT_LOG_PATH)
    #     self.assertEqual(lower > 0, True)
    #     self.assertEqual(lower <= total_weight, True)
    #     self.assertEqual(lower <= value, True)
    #     self.assertEqual(value <= total_weight, True)
    #     self.assertEqual(len(cut) > 1, True)


if __name__ == '__main__':
    unittest.main()
