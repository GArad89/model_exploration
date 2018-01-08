from abc import ABC, abstractmethod


class Cluster(ABC):

    @staticmethod
    def get_params():
        """
        Return json-schema and form describing the parameters this clustering algorithm accepts
        Json schema is standard, see documentation for jsonForm javascript library at for description of form
        Example at SpectralCluster
        """
        form = []
        schema = {}
        return schema, form

    @abstractmethod
    def cluster(self, dgraph):
        """Returns a list of set of states for dgraph
        sets can be joint
        """
        raise NotImplementedError




