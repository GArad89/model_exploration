import re
import string
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
from .label import DendrogramLabeler, labeling_on_type
from .RankingLabeler import RankingLabeler


class TfIdfLabeler(RankingLabeler):

    def __init__(self, graph, dendrogram, source):
        self.tfifd_labels_scores = {}
        super().__init__(graph, dendrogram, source)

    def get_edges_labels_list_in_super_node(self, super_node):
        return [self.graph.dgraph.edges[(edge[0], edge[1])].get('label','') for edge in super_node.projected_graph.edges()]

    def get_nodes_labels_list_in_super_node(self, super_node):
        return [self.graph.node_attr(node, 'label') for node in super_node.subset]

    def fill_ranking_dictionary_with_nodes(self):
        if(not self.tfifd_labels_scores):
            self.create_labels_score_dict()
        for super_node in self.dendrogram.nodes()[1:]:
            for node_item in super_node.projected_graph.dgraph.nodes(data=True):
                self.ranks_dict[node_item[0]] = self.tfifd_labels_scores[node_item[1].get('label','')]

    def fill_ranking_dictionary_with_edges(self):
        if(not self.tfifd_labels_scores):
            self.create_labels_score_dict()
        for super_node in self.dendrogram.nodes()[1:]:
            for edge_item in super_node.projected_graph.dgraph.edges(data=True):
                self.ranks_dict[(edge_item[0], edge_item[1])] = self.tfifd_labels_scores[edge_item[2].get('label','')]

    def create_labels_score_dict(self):
        # for every node, map list of labels of inside edges
        super_node_labels_dict = {}
        for super_node in self.dendrogram.nodes()[1:]:

            if(self.source == labeling_on_type.EDGES):
                super_node_labels_dict[super_node] = self.get_edges_labels_list_in_super_node(super_node)
            elif(self.source == labeling_on_type.NODES):
                super_node_labels_dict[super_node] = self.get_nodes_labels_list_in_super_node(super_node)
            else:
                nodes_labels = self.get_nodes_labels_list_in_super_node(super_node)
                edges_labels = self.get_edges_labels_list_in_super_node(super_node)
                super_node_labels_dict[super_node] = nodes_labels + edges_labels

        def tokenize(lst):
            tokens = []
            for s in lst:
                tokens = tokens + [s]
                #tokens = tokens + re.sub('[' + string.punctuation + ']', '', s).split()
            return tokens

        # learn important features
        corpus = map(list, super_node_labels_dict.values()) # transforms dict to list of lists
        vectorizer = TfidfVectorizer(preprocessor=lambda x: x, tokenizer=tokenize)
        vectorizer.fit_transform(corpus)

        # map every words to it's tfidf score
        self.tfifd_labels_scores = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))
        # print(self.tfifd_labels_scores)
        #
        #
        # unnamed_cluster = 1
        # def top_labels(nodes, n = 1): #TODO: support n top labels
        #
        #     nonlocal labels_dict
        #     nonlocal tfifd_scores
        #     nonlocal unnamed_cluster
        #
        #     nodes_labels = []
        #     for node in nodes:
        #         nodes_labels = nodes_labels + labels_dict[node]
        #
        #     print("available labels = ", nodes_labels)
        #
        #     labels = list(filter(lambda x: x[0] in nodes_labels, tfifd_scores.items()))
        #     # reveresed = [(x[1], x[0]) for x in labels].sort(reverse=True)
        #     if not len(labels):
        #         unnamed_cluster += 1
        #         return ["Unnamed {}".format(unnamed_cluster)]
        #     else:
        #         max_tfidf = max(labels, key=operator.itemgetter(1))[1]
        #         labels = list(filter(lambda x: x[1] == max_tfidf, labels))
        #         # labels = [nodes_labels.get(x[0]) for x in items]
        #         return [x[0] for x in labels]
        #
        # # label the dendrogram's nodes
        # for node in self.dendrogram.nodes():
        #     print(node.subset)
        #     top_label = top_labels(node.subset)
        #     print("top_label = ", top_label)
        #     node.label = super().shorten_label(top_label)
