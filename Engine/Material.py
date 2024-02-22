import numpy as np


class Material(object):
    def __init__(self):
        # This is an abstract class, so it does not need to have any attributes
        pass

    @property
    def name(self):
        return 'Material'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def get_elastic_matrix(self, *args) -> np.ndarray:
        raise NotImplementedError('Method not implemented')
