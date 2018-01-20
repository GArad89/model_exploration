import re
import string
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
from .label import GraphLabeler


class TfIdfLabeler(GraphLabeler):

    def __init__(self, graph, dendrogram, source):
        super().__init__(graph, dendrogram, source)

    def label(self):
        # for every node, map list of labels of inside edges
        labels_dict = {}
        for node in self.graph.nodes():
            node_labels = []
            for in_edge in self.graph.in_edges(node):

                edge_data = self.graph.get_edge_data(in_edge)
                if 'label' in edge_data:
                    node_labels.append(edge_data['label'])

            labels_dict[node] = node_labels

        def tokenize(lst):
            tokens = []
            for s in lst:
                tokens = tokens + [s]
                #tokens = tokens + re.sub('[' + string.punctuation + ']', '', s).split()
            return tokens

        # learn important features
        corpus = map(list, labels_dict.values()) # transforms dict to list of lists
        vectorizer = TfidfVectorizer(preprocessor=lambda x: x, tokenizer=tokenize)
        vectorizer.fit_transform(corpus)

        # map every words to it's tfidf score
        tfifd_scores = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))
        print(tfifd_scores)


        unnamed_cluster = 1
        def top_labels(nodes, n = 1): #TODO: support n top labels

            nonlocal labels_dict
            nonlocal tfifd_scores
            nonlocal unnamed_cluster

            nodes_labels = []
            for node in nodes:
                nodes_labels = nodes_labels + labels_dict[node]

            print("available labels = ", nodes_labels)

            labels = list(filter(lambda x: x[0] in nodes_labels, tfifd_scores.items()))
            # reveresed = [(x[1], x[0]) for x in labels].sort(reverse=True)
            if not len(labels):
                unnamed_cluster += 1
                return ["Unnamed {}".format(unnamed_cluster)]
            else:
                max_tfidf = max(labels, key=operator.itemgetter(1))[1]
                labels = list(filter(lambda x: x[1] == max_tfidf, labels))
                # labels = [nodes_labels.get(x[0]) for x in items]
                return [x[0] for x in labels]

        # label the dendrogram's nodes
        for node in self.dendrogram.nodes():
            print(node.subset)
            top_label = top_labels(node.subset)
            print("top_label = ", top_label)
            node.label = super().shorten_label(top_label)
