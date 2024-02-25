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

    def get_weights(self, number_gp: int) -> np.ndarray:
        """
        Returns the weights for numerical integration.

        Raises:
            NotImplementedError: Method not implemented.

        Returns:
            np.ndarray: Array of weights for numerical integration.
        """

        if number_gp == 1:
            return np.array([2.0])
        elif number_gp == 2:
            return np.array([1.0, 1.0])
        elif number_gp == 3:
            return np.array([5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0])
        elif number_gp == 4:
            return np.array([0.347854845137453857, 0.652145154862546142,
                             0.652145154862546142, 0.347854845137453857])
        elif number_gp == 5:
            return np.array([0.236926885056189087, 0.478628670499366468,
                             0.568888888888888888, 0.478628670499366468,
                             0.236926885056189087])
        else:
            raise NotImplementedError('Method not implemented')

    def get_points(self, number_gp: int) -> np.ndarray:
        """
        Returns the points for numerical integration.

        Raises:
            NotImplementedError: Method not implemented.

        Returns:
            np.ndarray: Array of points for numerical integration.
        """
        if number_gp == 1:
            return np.array([0.0])
        elif number_gp == 2:
            return np.array([-1.0 / np.sqrt(3), 1.0 / np.sqrt(3)])
        elif number_gp == 3:
            return np.array([-.2 * np.sqrt(15), 0.0, .2 * np.sqrt(15)])
        elif number_gp == 4:
            return np.array([-0.861136311594052575, -0.339981043584856264,
                             0.339981043584856264, 0.861136311594052575])
        else:
            raise NotImplementedError('Method not implemented')

    def get_ordered_points(self, number_gp: int) -> np.ndarray:
        """ Returns the points for numerical integration in an ordered manner."""
        if number_gp == 1:

            gauss_points = self.get_points(1)

            return np.array([[gauss_points[0], gauss_points[0]]])

        elif number_gp == 2:
            gauss_points = self.get_points(2)

            # Extract min and max values along xi and eta axes
            min_xi, max_xi = min(gauss_points), max(gauss_points)
            min_eta, max_eta = min(gauss_points), max(gauss_points)

            # Form arranged_gauss_points based on the min and max values
            arranged_gauss_points = np.array([
                [min_xi, min_eta],
                [max_xi, min_eta],
                [max_xi, max_eta],
                [min_xi, max_eta]
            ])

            return arranged_gauss_points

        elif number_gp == 3:
            gauss_points = self.get_points(3)

            # Extract min and max values along xi and eta axes
            min_xi, max_xi = min(gauss_points), max(gauss_points)
            min_eta, max_eta = min(gauss_points), max(gauss_points)
            central_point = gauss_points[1]

            # Form arranged_gauss_points based on the min and max values
            arranged_gauss_points = np.array([
                [min_xi, min_eta],
                [central_point, min_eta],
                [max_xi, min_eta],
                [min_xi, central_point],
                [central_point, central_point],
                [max_xi, central_point],
                [min_xi, max_eta],
                [central_point, max_eta],
                [max_xi, max_eta]
            ])

            return arranged_gauss_points
        else:
            raise NotImplementedError('Method not implemented')
