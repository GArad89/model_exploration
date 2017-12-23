import numpy as np
from scipy.optimize import linprog
import networkx as nx
import sys
import math

# Embeddings import:
from gem.embedding.gf import GraphFactorization
from gem.embedding.lap import LaplacianEigenmaps
from gem.embedding.lle import LocallyLinearEmbedding
from gem.embedding.hope import HOPE
from gem.embedding.node2vec import node2vec


def compute_lower_bound(G, partial_assignment_dict={}):

    ## partial_assignment - a dictionary mapping node indexes
    ## assumsing nodes are partitioned to S and S_hat, where partial_assignment_dict[n] == 1 if n in S
    ## unassigned nodes should not be included in the dict

    edge = G.edges()
    weights = nx.get_edge_attributes(G, "weight")

    N = len(G.nodes()) #+2

    # Add weight constraints
    C = np.zeros(shape=(1, N ** 2))

    #putting all nodes in a dictionary. in order to remove assumption that all node names are numbers.
    #dic[1st_node]=0 , dic[2nd_node]=1 and so on.
    i=0
    dic={}
    for node in G.nodes():
        dic[str(node)]=i
        i+=1

    ## Minimize sum_(i,j) c_(i,j) d_(u,v)
    for e in edge:
        C[0][N * (dic[str(e[0])]) + (dic[str(e[1])])] = weights.get(e,1)
        C[0][N * (dic[str(e[1])]) + (dic[str(e[0])])] = weights.get(e,1)

    for n1 in partial_assignment_dict:
##        if(partial_assignment_dict[n1]==1):
##            C[0][N * dic[str(n1)] + N-1] = sys.maxsize
##            C[0][N * (N-1) + dic[str(n1)]] = sys.maxsize
##        if(partial_assignment_dict[n1]==0):
##            C[0][N * dic[str(n1)] + N-2] = sys.maxsize
##            C[0][N * (N-2) + dic[str(n1)]] = sys.maxsize
            
        for n2 in partial_assignment_dict:
            if n1 != n2:
                if partial_assignment_dict[n1] == partial_assignment_dict[n2]:
                    C[0][N * dic[str(n1)] + dic[str(n2)]] = sys.maxsize
                    C[0][N * dic[str(n2)] + dic[str(n1)]] = sys.maxsize

    ## S.T. traingle inquality
    A1 = None
    for i in range(N):
        for j in range(N):
            if i == j:
                row = np.zeros(shape=(1, N ** 2))
                row[0][i * N + j] = -1
                if A1 is None:
                    A1 = row
                else:
                    A1 = np.concatenate((A1, row))
            else:
                for k in range(N):
                    if k == j:  # this contraint will be added by the i==j case
                        continue
                    row = np.zeros(shape=(1, N ** 2))
                    row[0][i * N + k] += 1
                    row[0][i * N + j] += -1
                    row[0][j * N + k] += -1
                    A1 = np.concatenate((A1, row))
            #print(row)

    B1 = np.zeros(shape=(A1.shape[0], 1))

    ## Demands constraints
    A2 = np.ones(shape=(1, N ** 2))
    for i in range(N):
        A2[0][i * N + i] = 0
    #print(A2)
      
    B2 = np.ones(shape=(1, 1))
##    for i in range(N):
##        for j in range(N):
##            if(j>i):
##                row=np.zeros(shape=(1, N ** 2))
##                row[0][i*N+j]=1
##                row[0][j*N+i]=-1
##                A2=np.concatenate((A2, row))
##                B2=np.concatenate((B2, np.zeros(shape=(1, 1))))
    #print(B2)

    res = linprog(C[0], A_ub=A1, b_ub=B1, A_eq=A2, b_eq=B2, bounds=(0, None),options={'maxiter':20,'tol':0.4,'bland':True})
    #print('Optimal value:', res.fun, '\nX:', res.x)
    return res


def compute_cut_value(G, cut):
    cut_dic = {}
    s_cut_nodes = 0
    for i in G.nodes():
        if cut[i]:
            cut_dic[i] = 0
            s_cut_nodes += 1
        else:
            cut_dic[i] = 1

    cut_weight = 0
    weights = nx.get_edge_attributes(G, 'weight')
    for e in G.edges():
        if cut_dic[e[0]] != cut_dic[e[1]]:
            cut_weight += weights.get(e)

    if min(s_cut_nodes, len(G.nodes()) - s_cut_nodes) == 0:
        return math.inf
    return float(cut_weight) / min(s_cut_nodes, len(G.nodes()) - s_cut_nodes)


def compute_total_edges_wieght(G):

    total_weight = 0
    weights = nx.get_edge_attributes(G, 'weight')
    for e in G.edges():
        total_weight += weights.get(e)
    return total_weight


def generate_cut_from_relaxed_solution(d, org_G, partial_assignment_dict = {}):

    ## partial_assignment - a dictionary mapping node indexes
    ## assumsing nodes are partitioned to S and S_hat, where partial_assignment_dict[n] == 1 if n in S
    ## unassigned nodes should not be included in the dict
    G = nx.DiGraph()
    N = int(len(d) ** 0.5)
    for i in range(N):
        G.add_node(i)

    for i in range(N):
        for j in range(N):
            G.add_edge(i, j, weight=d[i * N + j])

    embedding_space = 1
    models = get_embeddings(embedding_space)
    # Try different embeddings
    i = 0
    best_cut_value = compute_total_edges_wieght(org_G) + 1
    best_cut = None
    for embedding in models:
        print('Trying embedding method: ', embedding._method_name)
        Y, t = embedding.learn_embedding(graph=G, edge_f=None, is_weighted=True, no_python=True)
        sorted_values = np.unique(Y)
        print(Y) 
        # Try ALL possible threshold cuts - see lecture notes:
        # Sparsest Cut Computational and Metric Geometry Instructor: Yury Makarychev
        for v in sorted_values[:-1]:
            st = ""
            node_id = 0
            current_cut = []

            for node in Y > v:
                if partial_assignment_dict.get(i) == 0:
                    current_cut.append(False)
                elif partial_assignment_dict.get(i):
                    
                    current_cut.append(True)
                    st += str(node_id) + ", "
                else:
                    current_cut.append(node[0])
                    if node[0]:
                        st += str(node_id) + ", "
                node_id += 1

            val = compute_cut_value(org_G, current_cut)
            if val < best_cut_value:
                best_cut_value = val
                best_cut = current_cut
            print("[", st, "]:", val)
        i += 1

    return best_cut, best_cut_value



def get_embeddings(embedding_space):
    models = []
    # You can comment out the methods you don't want to run
    models.append(GraphFactorization(embedding_space, 100000, 1 * 10 ** -4, 1.0))
    models.append(LaplacianEigenmaps(embedding_space))
    models.append(LocallyLinearEmbedding(embedding_space))
    # Embeddings I was unable to get working yet - it seems that HOPE converts k to k+1 for some reason....
    # models.append(HOPE(k + 1, 0.01))
    # models.append(node2vec(k, 1, 80, 10, 10, 1, 1))
    # models.append(SDNE(d=2, beta=5, alpha=1e-5, nu1=1e-6, nu2=1e-6, K=3,n_units=[50, 15,], rho=0.3, n_iter=50, xeta=0.01,n_batch=500,
    #                modelfile=[base_path + '/intermediate/enc_model.json', base_path + '/intermediate/dec_model.json'],
    #                weightfile=[base_path + '/intermediate/enc_weights.hdf5', base_path + '/intermediate/dec_weights.hdf5']))
    return models

