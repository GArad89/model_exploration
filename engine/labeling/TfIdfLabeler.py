import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from .label import GraphLabeler


class TfIdfLabeler(GraphLabeler):

    def __init__(self, graph, dendrogram):
        super().__init__(graph, dendrogram)

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

        print(labels_dict)

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

            top_label = None
            top_labels_score = -1
            for label in nodes_labels:
                if tfifd_scores[label] > top_labels_score:
                    top_labels_score = tfifd_scores[label]
                    top_label = label

            if top_label:
                tfifd_scores[top_label] = -1
            else:
                top_label = "Unnamed {}".format(unnamed_cluster)
                unnamed_cluster += 1

            return top_label

        # label the dendrogram's nodes
        for node in self.dendrogram.nodes():
            print(node.subset)
            top_label = top_labels(node.subset)
            print("top_label = ", top_label)
            node.label = top_label
