from .label import *
import os


class PrefixLabeler(GraphLabeler):

    def __init__(self, graph, dendrogram, source = labeling_on_type.EDGES_AND_NODES):
        super().__init__(graph, dendrogram, source)

    def label(self):
        unnamed_cluster = 1
        # label the dendrogram's nodes
        for node in self.dendrogram.nodes()[1:]:
            labels = super().get_labels(node)

            # shortest common prefix 
            prefix = os.path.commonprefix(list(labels))
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
