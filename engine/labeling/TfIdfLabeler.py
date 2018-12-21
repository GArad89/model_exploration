import re
import string
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
from .label import DendrogramLabeler, labeling_on_type
from .RankingLabeler import RankingLabeler


class TfIdfLabeler(RankingLabeler):

    def __init__(self, graph, dendrogram, source, max_labels=3, unify_prefix=True):
        self.tfifd_labels_scores = {}
        super().__init__(graph, dendrogram, source, max_labels, unify_prefix)

    def is_ordered_labeler(self):
        return False

    def _get_edges_labels_list_in_super_node(self, super_node):
        return [self.graph.dgraph.edges[(edge[0], edge[1])].get('label','') for edge in super_node.projected_graph.edges()]

    def _get_nodes_labels_list_in_super_node(self, super_node):
        return [self.graph.node_attr(node, 'label') for node in super_node.subset]

    def fill_ranking_dictionary_with_nodes(self):
        if not self.tfifd_labels_scores:
            self.create_labels_score_dict()
        for super_node in self.dendrogram.nodes()[1:]:
            for node_item in super_node.projected_graph.dgraph.nodes(data=True):
                self.ranks_dict[node_item[0]] = self.tfifd_labels_scores[node_item[1].get('label','')]

    def fill_ranking_dictionary_with_edges(self):
        if not self.tfifd_labels_scores:
            self.create_labels_score_dict()
        for super_node in self.dendrogram.nodes()[1:]:
            for edge_item in super_node.projected_graph.dgraph.edges(data=True):
                self.ranks_dict[(edge_item[0], edge_item[1])] = self.tfifd_labels_scores[edge_item[2].get('label','')]

    def create_labels_score_dict(self):
        # for every node, map list of labels of inside edges
        super_node_labels_dict = {}
        for super_node in self.dendrogram.nodes()[1:]:

            if self.source == labeling_on_type.EDGES:
                super_node_labels_dict[super_node] = self._get_edges_labels_list_in_super_node(super_node)
            elif self.source == labeling_on_type.NODES:
                super_node_labels_dict[super_node] = self._get_nodes_labels_list_in_super_node(super_node)
            else:
                nodes_labels = self._get_nodes_labels_list_in_super_node(super_node)
                edges_labels = self._get_edges_labels_list_in_super_node(super_node)
                super_node_labels_dict[super_node] = nodes_labels + edges_labels

        def tokenize(lst):
            tokens = []
            for s in lst:
                tokens.append(s) # TODO should be: tokens = tokens + re.sub('[' + string.punctuation + ']', '', s).split()
                                 # but need need to map back to original labels
            return tokens

        # learn important features
        corpus = map(list, super_node_labels_dict.values()) # transforms dict to list of lists
        vectorizer = TfidfVectorizer(preprocessor=lambda x: x, tokenizer=tokenize)
        vectorizer.fit_transform(corpus)

        # map every words to it's tfidf score
        self.tfifd_labels_scores = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))
