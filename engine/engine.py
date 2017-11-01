from graph import *

def is_simple(dgraph):
    pass #TODO

def cluster(dgraph):
    pass #TODO

def partition(dgraph, states):
    projected_graph = dgraph.project(states)

    if is_simple(projected_graph):
        return

    clusters = cluster(projected_graph)
    for clutser in clusters:
        partition(dgraph, cluster)
