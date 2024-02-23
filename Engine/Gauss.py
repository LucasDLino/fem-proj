import numpy as np


class Gauss(object):
    """
    Represents a Gauss quadrature method for numerical integration.

    This class provides methods to retrieve the weights and points of the Gauss quadrature.

    Attributes:
        None

    Usage:
        gauss = Gauss()

        weights = gauss.get_weights()

        points = gauss.get_points()
    """

    def __init__(self):
        """
        Initializes a Gauss object.
        """
        pass

    @property
    def name(self) -> str:
        """
        Returns the name of the Gauss quadrature method.

        Returns:
            str: The name of the Gauss quadrature method.
        """
        return 'Gauss'

    def __str__(self) -> str:
        """
        Returns a string representation of the Gauss object.

        Returns:
            str: String representation of the Gauss object.
        """
        return self.name

    def __eq__(self, other) -> bool:
        """
        Checks if two Gauss objects are equal.

        Args:
            other (Gauss): Another Gauss object to compare.

        Returns:
            bool: True if the Gauss objects are equal, False otherwise.
        """
        return self.name == other.name

    def __hash__(self) -> int:
        """
        Computes the hash value of the Gauss object.

        Returns:
            int: Hash value of the Gauss object.
        """
        return hash(self.name)

    def get_weights(self, gauss_points: int) -> np.ndarray:
        """
        Returns the weights for numerical integration.

        Raises:
            NotImplementedError: Method not implemented.

        Returns:
            np.ndarray: Array of weights for numerical integration.
        """

        if gauss_points == 1:
            return np.array([2.0])
        elif gauss_points == 2:
            return np.array([1.0, 1.0])
        elif gauss_points == 3:
            return np.array([5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0])
        elif gauss_points == 4:
            return np.array([0.347854845137453857, 0.652145154862546142,
                             0.652145154862546142, 0.347854845137453857])
        elif gauss_points == 5:
            return np.array([0.236926885056189087, 0.478628670499366468,
                             0.568888888888888888, 0.478628670499366468,
                             0.236926885056189087])
        else:
            raise NotImplementedError('Method not implemented')

    def get_points(self, gauss_points: int) -> np.ndarray:
        """
        Returns the points for numerical integration.

        Raises:
            NotImplementedError: Method not implemented.

        Returns:
            np.ndarray: Array of points for numerical integration.
        """
        if gauss_points == 1:
            return np.array([0.0])
        elif gauss_points == 2:
            return np.array([-1.0 / np.sqrt(3), 1.0 / np.sqrt(3)])
        elif gauss_points == 3:
            return np.array([-.2 * np.sqrt(15), 0.0, .2 * np.sqrt(15)])
        elif gauss_points == 4:
            return np.array([-0.861136311594052575, -0.339981043584856264,
                             0.339981043584856264, 0.861136311594052575])
        else:
            raise NotImplementedError('Method not implemented')
