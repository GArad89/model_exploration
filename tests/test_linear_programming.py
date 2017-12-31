import networkx as nx
import engine.linear_programming.lin_prog_solver as lps
import matplotlib.pyplot as plt
import sys

def generate_toy_example(draw=False):
    G = nx.Graph()
    G.add_node(0, label="A", attr="A")
    G.add_node(1, label="B", attr="B")
    G.add_node(2, label="C", attr="C")
    G.add_node(3, label="D", attr="D")
    G.add_edge(0, 1, weight=2)
    G.add_edge(0, 2, weight=1)
    G.add_edge(1, 2, weight=4)
    G.add_edge(0, 3, weight=8)

    pos = nx.spring_layout(G)  # positions for all nodes
    # add nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)
    # add edges
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_edge_labels(G, pos, font_size=5, font_family='sans-serif', label_pos=0.3)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    if draw:
        plt.show()

    return G

def test_linear_programming():
    # case 1
    G = generate_toy_example()
    res = lps.compute_lower_bound(G)
    cut, value = lps.generate_cut_from_relaxed_solution(res.x, G)
    print("best cut:", cut, "value:", value)

    # case 2
    G = generate_toy_example()
    partial_assignment_dict = {0: 1, 2: 1}
    res = lps.compute_lower_bound(G, partial_assignment_dict)
    cut, value = lps.generate_cut_from_relaxed_solution(res.x, G, partial_assignment_dict)
    print("best cut:", cut, "value:", value)
