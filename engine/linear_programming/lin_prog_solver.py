from FileWriter import log

import numpy as np
from scipy.optimize import linprog
import networkx as nx
import sys
import math
from enum import Enum

# Embeddings import:
from gem.embedding.gf import GraphFactorization
from gem.embedding.lap import LaplacianEigenmaps
from gem.embedding.lle import LocallyLinearEmbedding
from gem.embedding.hope import HOPE
from gem.embedding.node2vec import node2vec


class EMEDDINGS(Enum):

    GRAPH_FACTORIZATIONE_MBEDDINGS = 0
    LAPLACIAN_EIGENMAPS_EMBEDDINGS = 1
    LOCALLY_LINEAR_EMBEDDING = 2
    HOPE_EMBEDDING = 3
    NODE2VEC_EMBEDDING_EMBEDDINGS = 4
    SDNE_EMBEDDING_EMBEDDINGS = 5


class LPS:
    P0 = 'p_0'
    P1 = 'p_1'

    def __init__(self, embeddings=[]):

        self.embeddings = embeddings
        if len(embeddings) == 0:
            embeddings.append(EMEDDINGS.GRAPH_FACTORIZATIONE_MBEDDINGS)
            embeddings.append(EMEDDINGS.LAPLACIAN_EIGENMAPS_EMBEDDINGS)
            embeddings.append(EMEDDINGS.LOCALLY_LINEAR_EMBEDDING)

        for i in embeddings:
            if i not in list(EMEDDINGS):
                raise ValueError("Illegal embedding chosen" + str(i))

    def _get_embeddings(self, embedding_space):

        # You can comment out the methods you don't want to run
        models = list()
        for embed_method in self.embeddings:
            if embed_method == EMEDDINGS.GRAPH_FACTORIZATIONE_MBEDDINGS:
                models.append(GraphFactorization(embedding_space, 100000, 1 * 10 ** -4, 1.0))
            if embed_method == EMEDDINGS.LAPLACIAN_EIGENMAPS_EMBEDDINGS:
                models.append(LaplacianEigenmaps(embedding_space))
            if embed_method == EMEDDINGS.LOCALLY_LINEAR_EMBEDDING:
                models.append(LocallyLinearEmbedding(embedding_space))
            if embed_method == EMEDDINGS.HOPE_EMBEDDING:
                models.append(HOPE(2 + 1, 0.01))
            if embed_method == EMEDDINGS.NODE2VEC_EMBEDDING_EMBEDDINGS:
                models.append(node2vec(2, 1, 80, 10, 10, 1, 1))
            # Embeddings I was unable to get working yet - it seems that HOPE converts k to k+1 for some reason....
            # if embed_method == EMEDDINGS.SDNE_EMBEDDING_EMBEDDINGS:
            #     models.append(SDNE(d=2, beta=5, alpha=1e-5, nu1=1e-6, nu2=1e-6, K=3,n_units=[50, 15,], rho=0.3, n_iter=50, xeta=0.01,n_batch=500,
            #                modelfile=[base_path + '/intermediate/enc_model.json', base_path + '/intermediate/dec_model.json'],
            #                weightfile=[base_path + '/intermediate/enc_weights.hdf5', base_path + '/intermediate/dec_weights.hdf5']))
        return models

    @staticmethod
    def _compute_LP_lower_bound(G, log_path=None):
        '''
        partial_assignment - a dictionary mapping node indexes
        assumsing nodes are partitioned to S and S_hat, where partial_assignment_dict[n] == 1 if n in S
        unassigned nodes should not be included in the dict
        '''
        N = len(G.nodes())
        node2ind = {}
        for i, n in enumerate(G.nodes()):
            node2ind[str(n)] = i

        weights = nx.get_edge_attributes(G, "weight")

        # Add weight constraints
        C = np.zeros(shape=(1, N ** 2))

        ## Minimize sum_(i,j) c_(i,j) d_(u,v)
        for e in G.edges():
            C[0][N * node2ind[str(e[0])] + node2ind[str(e[1])]] = weights[e]
            # C[0][N * node2ind[str(e[1])] + node2ind[str(e[0])]] = weights[e]

        ## s.t. traingle inquality: d_i,w + d_w,j >= d_i,j && dxy > 0
        A1 = None
        for i in range(N):
            for j in range(N):
                for w in range(N):
                    row = np.zeros(shape=(1, N ** 2))
                    row[0][i * N + w] += -1
                    row[0][w * N + j] += -1
                    row[0][i * N + j] += 1
                    if A1 is None:
                        A1 = row
                    else:
                        A1 = np.concatenate((A1, row))

        B1 = np.zeros(shape=(A1.shape[0], 1))

        # d_x,x = 0
        B2 = np.zeros(shape=(N, 1))
        A2 = None
        for i in range(N):
            row = np.zeros(shape=(1, N ** 2))
            row[0][i + i * N] = 1
            if A2 is None:
                A2 = row
            else:
                A2 = np.concatenate((A2, row))

        # d_xy = d_yx
        A3 = None
        B3 = None
        for i in range(N):
            for j in range(N):
                if i >= j:
                    continue
                row = np.zeros(shape=(1, N ** 2))
                row[0][i * N + j] = 1
                row[0][j * N + i] = -1
                row_v = np.zeros(shape=(1, 1))
                if A3 is None:
                    A3 = row
                    B3 = row_v
                else:
                    A3 = np.concatenate((A3, row))
                    B3 = np.concatenate((B3, row_v))

        A2 = np.concatenate((A3, A2))
        B2 = np.concatenate((B3, B2))

        # sum_(x, y) d_x,x = n
        B3 = N * np.ones(shape=(1, 1))
        A3 = np.ones(shape=(1, N ** 2))

        A2 = np.concatenate((A3, A2))
        B2 = np.concatenate((B3, B2))

        res = linprog(C[0], A_ub=A1, b_ub=B1, A_eq=A2, b_eq=B2, bounds=(0, None), method='simplex')  # 'interior-point'
        msg = 'Optimal value:' + str(res.fun) + '\nX:' + str(res.x)
        log(msg, log_path)
        return res

    @staticmethod
    def _compute_cut_value(G, cut):

        cut_dic = {}
        s_cut_nodes = 0
        for i in G.nodes():
            if str(i) in cut:
                cut_dic[str(i)] = 0
                s_cut_nodes += 1
            else:
                cut_dic[str(i)] = 1

        cut_weight = 0
        weights = nx.get_edge_attributes(G, 'weight')
        for e in G.edges():
            if cut_dic[str(e[0])] != cut_dic[str(e[1])]:
                cut_weight += weights.get(e)

        if min(s_cut_nodes, len(G.nodes()) - s_cut_nodes) == 0:
            return math.inf
        return float(cut_weight) / min(s_cut_nodes, len(G.nodes()) - s_cut_nodes)

    @staticmethod
    def _compute_total_edges_wieght(G):

        total_weight = 0
        weights = nx.get_edge_attributes(G, 'weight')
        for e in G.edges():
            total_weight += weights.get(e)
        return total_weight

    @staticmethod
    def _flip_dic(nodes_mapping):

        dic_ = {}
        for v, k in nodes_mapping.items():
            if k not in dic_:
                dic_[k] = []
            dic_[k].append(v)
        return dic_

    @staticmethod
    def _to_string_cut(best_cut):
        cut_mapping_to_org_nodes = []
        for v in best_cut:
            cut_mapping_to_org_nodes.append(str(v))
        return ",".join(cut_mapping_to_org_nodes)

    def _generate_cut_from_relaxed_solution(self, X, org_G, log_path=None):
        '''
        partial_assignment - a dictionary mapping node indexes
        assumsing nodes are partitioned to S and S_hat, where partial_assignment_dict[n] == 1 if n in S
        unassigned nodes should not be included in the dict
        :param X:
        :param org_G:
        :param log_path:
        :return:
        '''

        ind2node = {}
        for i, n in enumerate(org_G.nodes()):
            ind2node[i] = str(n)

        G = LPS.metric_to_graph(X)

        embedding_space = 1
        models = self._get_embeddings(embedding_space)
        # Try different embeddings
        i = 0
        best_cut_value = LPS._compute_total_edges_wieght(org_G) + 1
        best_cut = None
        for embedding in models:
            msg = 'Trying embedding method: ' + embedding._method_name
            log(msg, log_path)
            Y, t = embedding.learn_embedding(graph=G, edge_f=None, is_weighted=True, no_python=True)
            log(str(Y), log_path)
            sorted_values = np.unique(Y)

            # Try ALL possible threshold cuts - see lecture notes:
            # Sparsest Cut Computational and Metric Geometry Instructor: Yury Makarychev
            for v in sorted_values[:-1]:
                node_id = 0
                current_cut = []
                for node in Y > v:
                    if node[0]:
                        current_cut.append(str(ind2node[node_id]))
                    node_id += 1

                if LPS.P0 in current_cut and LPS.P1 in current_cut:
                    c1 = current_cut.copy()
                    c1.remove(LPS.P0)
                    v1 = LPS._compute_cut_value(org_G, c1)
                    c2 = current_cut.copy()
                    c2.remove(LPS.P1)
                    v2 = LPS._compute_cut_value(org_G, c2)
                    val = max(v1, v2)
                    current_cut = c1 if v1 > v2 else c2
                else:
                    val = LPS._compute_cut_value(org_G, current_cut)

                if val < best_cut_value:
                    best_cut_value = val
                    best_cut = current_cut
                    best_cut_method = embedding._method_name
                msg = "[" + LPS._to_string_cut(current_cut) + "]:" + str(val) + " - "
                log(msg, log_path)
            i += 1

        msg = "BEST Solution: [" + LPS._to_string_cut(current_cut) + "]:" + str(
            best_cut_value) + " - " + best_cut_method
        log(msg, log_path)
        return best_cut, best_cut_value

    @staticmethod
    def metric_to_graph(X):
        '''
        Returns a graph, where the weight of an edge represents the similarity between the nodes
        Note, that since X includes distances, it needs to be transformed and normalized to a similarity meausre
        Assumption: X is a metric
        :param X:
        :return: G - where edges represent node similarity
        '''
        max_val = max(max(X), 1.0)  # normalize weights
        G = nx.Graph()
        N = int(len(X) ** 0.5)
        for i in range(N):
            G.add_node(i)
        for i in range(N):
            for j in range(N):
                if i > j:
                    continue
                if X[i * N + j] > 0:
                    G.add_edge(i, j, weight=(max_val - X[i * N + j]) / max_val)
                else:
                    G.add_edge(i, j, weight=1.0)
        return G

    @staticmethod
    def _graph_to_standard_form(G, partial_assignment):

        i = 0
        dic = {}
        reg_G = nx.Graph()
        if len(partial_assignment) > 0:
            reg_G.add_node(LPS.P0)
            reg_G.add_node(LPS.P1)
        for node in G.nodes():
            if node not in partial_assignment:
                dic[str(node)] = str(i)
                reg_G.add_node(str(i))
                i += 1
            else:
                dic[str(node)] = "p_0" if partial_assignment.get(node) else "p_1"

        edges = nx.get_edge_attributes(G, 'weight')
        edges_combined = {}
        for e, v in edges.items():
            s = dic[str(e[0])]
            t = dic[str(e[1])]
            if s == t:  # ignoring self loops!
                continue
            if s > t:
                edges_combined[(t, s)] = edges_combined.get((t, s), 0) + v
            else:
                edges_combined[(s, t)] = edges_combined.get((s, t), 0) + v

        for e, v in edges_combined.items():
            if e[0] == e[1]:
                continue
            if (e[0] == "p_0" and e[1] == "p_1") or (e[0] == "p_1" and e[1] == "p_0"):
                # skips edges connected the partitions, this is done to guide the algorithm not to join the two
                # partitions; it is also crucial for the lower bound to be correct
                continue
            reg_G.add_edge(e[0], e[1], weight=v)

        return reg_G, dic

    @staticmethod
    def _compute_partial_assignment_cost(G, partial_assignment):

        weights = nx.get_edge_attributes(G, 'weight')
        partial_cut_weight = 0
        p1_nodes = 0
        p2_nodes = 0
        for x in partial_assignment:
            if x:
                p1_nodes += 1
            else:
                p2_nodes += 1
        N = len(G.nodes())
        for x in partial_assignment:
            for y in partial_assignment:
                if x < y:
                    v1 = partial_assignment[x]
                    v2 = partial_assignment[y]
                    if v1 != v2:
                        partial_cut_weight += weights.get((x, y), 0)
                        partial_cut_weight += weights.get((y, x), 0)

        left_nodes = N - p1_nodes - p2_nodes
        mid = int(min(N / 2, p1_nodes + left_nodes,
                      p2_nodes + left_nodes))  # the denominator can be smaller than the following term
        return partial_cut_weight / float(mid)

    def solve(self, G, partial_assignment_dict={}, log_path=None):

        reg_G, old_nodes_to_new_nodes = LPS._graph_to_standard_form(G, partial_assignment_dict)
        res = LPS._compute_LP_lower_bound(reg_G, log_path)
        lower_bound = res.fun + LPS._compute_partial_assignment_cost(G, partial_assignment_dict)
        cut, value = self._generate_cut_from_relaxed_solution(res.x, reg_G, log_path)
        new_cut = []
        new_node_to_old_nodes = self._flip_dic(old_nodes_to_new_nodes)
        for x in cut:
            new_cut.extend(new_node_to_old_nodes[x])
        real_value = self._compute_cut_value(G, new_cut)
        return lower_bound, new_cut, real_value
