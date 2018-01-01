import networkx as nx
import matplotlib.pyplot as plt


def draw(G, output_path = None):

    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx_nodes(G, pos, node_size=700) # add nodes
    nx.draw_networkx_edges(G, pos, width=2) # add edges
    nx.draw_networkx_edge_labels(G, pos, font_size=5, font_family='sans-serif', label_pos=0.3)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    if output_path:
        plt.savefig(output_path)


def write_nx_graph_to_file(G, output_folder, dot_path ='graph.dot'):
    nx.drawing.nx_pydot.write_dot(G, output_folder + dot_path)