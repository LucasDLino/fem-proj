import numpy as np


class Material(object):
    """
    Represents a material used in structural analysis.

    This is an abstract class defining the interface for material properties.

    """

    def __init__(self):
        """Initializes a Material object."""
        # This is an abstract class, so it does not need to have any attributes
        pass

    @property
    def name(self):
        """Returns the name of the material."""
        return 'Material'

    def __str__(self):
        """Returns a string representation of the material."""
        return self.name

    def __eq__(self, other):
        """Compares if two materials are equal based on their names."""
        return self.name == other.name

    def __hash__(self):
        """Returns the hash value of the material based on its name."""
        return hash(self.name)

    def get_elastic_matrix(self, *args) -> np.ndarray:
        """
        Computes the elastic matrix of the material.

        Args:
            \*args: Additional arguments if needed.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.

        """
        raise NotImplementedError('Method not implemented')
