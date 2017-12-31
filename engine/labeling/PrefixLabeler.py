from .label import GraphLabeler
import os
import itertools

class PrefixLabeler(GraphLabeler):

    def __init__(self, graph, dendrogram):
        super().__init__(graph, dendrogram)

    def label(self):
        unnamed_cluster = 1
        # label the dendrogram's nodes
        for node in self.dendrogram.nodes()[1:]:
            subgraph = node.projected_graph.dgraph
            # get all inner labels (nodes and edges)
            labels = [attrs.get('label','') for _, attrs in 
                        itertools.chain(subgraph.edges.items(), subgraph.nodes.items())]
            # filter out empty ones
            labels = list(filter(None, labels))
            # uniqify
            labels = set(labels)

            # shortest common prefix 
            prefix = os.path.commonprefix(labels)
            if not prefix:
                # NOTE ESCAPED \n for graphviz happiness
                node.label = "\n".join(labels)
            else:
                #TODO: deal with empty suffix and repeated labels
                node.label = "{prefix}{{\n{suffixes}}}".format(
                    prefix=prefix,
                    suffixes=",\n".join(l[len(prefix):] for l in labels)
                    )

            if not node.label:
                #TODO:roee(hack)
                node.label = "Unnamed {}".format(unnamed_cluster)
                unnamed_cluster += 1
