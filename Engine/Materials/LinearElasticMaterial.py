from Engine.Material import Material
import numpy as np


class LinearElasticMaterial(Material):
    """
    Represents a linear elastic material.

    Attributes:
        young_modulus (float): Young's modulus of the material.

        poisson_ratio (float): Poisson's ratio of the material.

        _beam_thickness (float): Thickness of the beam.

    """

    def __init__(self, young_modulus: float, poisson_ratio: float):
        """
        Initializes a LinearElasticMaterial object.

        Args:
            young_modulus (float): Young's modulus of the material.

            poisson_ratio (float): Poisson's ratio of the material.
        """
        super().__init__()
        self.young_modulus = young_modulus
        self.poisson_ratio = poisson_ratio
        self._beam_thickness = 1.0

    @property
    def name(self):
        """Returns the name of the material."""
        return 'Elastic Linear Material'

    @property
    def beam_thickness(self) -> float:
        """Getter method for beam thickness."""
        return self._beam_thickness

    @beam_thickness.setter
    def beam_thickness(self, new_thickness: float):
        """Setter method for beam thickness."""
        self._beam_thickness = new_thickness

    def get_elastic_matrix(self, plane_stress: bool = False) -> np.ndarray:
        """
        Returns the elastic matrix of the material.

        Args:
            plane_stress (bool): Flag indicating whether the stress state is plane stress.

        Returns:
            np.ndarray: Elastic matrix of the material.
        """
        if plane_stress:
            return self._get_plane_stress_matrix()
        else:
            return self._get_plane_strain_matrix()

    def _get_plane_stress_matrix(self) -> np.ndarray:
        """
        Returns the plane stress elastic matrix.

        Returns:
            np.ndarray: Plane stress elastic matrix.
        """
        poisson = self.poisson_ratio
        young = self.young_modulus
        factor = young / (1 - poisson ** 2)
        matrix = np.array([[1, poisson, 0.],
                           [poisson, 1., 0.],
                           [0., 0., (1. - poisson) / 2]])
        return factor * matrix

    def _get_plane_strain_matrix(self) -> np.ndarray:
        """
        Returns the plane strain elastic matrix.

        Returns:
            np.ndarray: Plane strain elastic matrix.
        """
        poisson = self.poisson_ratio
        young = self.young_modulus
        factor = young / ((1 + poisson) * (1 - 2 * poisson))
        matrix = np.array([[1 - poisson, poisson, 0.],
                           [poisson, 1 - poisson, 0.],
                           [0., 0., (1 - 2 * poisson) / 2]])
        return factor * matrix
