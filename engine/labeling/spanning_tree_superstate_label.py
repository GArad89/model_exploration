import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from .superstate_label import SuperstateGraphLabeler
from ..baisc_entities.graph import *

class STLabeling(SuperstateGraphLabeler):
    def __init__(self, graph, superstates):
        super().__init__(graph, superstates)

    def label(self):
        pass

    def get_label_for_subset(self,subset):
        pass
