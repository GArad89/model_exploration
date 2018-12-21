
import os
import shutil
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt

def project_root():
    "Get project root path"
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


RANDOM_SEED = 42
def test_init_seed():
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)


def delete_files_from_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


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