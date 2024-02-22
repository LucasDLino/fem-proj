from Engine.Material import Material
import numpy as np


class LinearElasticMaterial(Material):
    def __init__(self, young_modulus: float, poisson_ratio: float):
        super().__init__()
        self.young_modulus = young_modulus
        self.poisson_ratio = poisson_ratio
        self._beam_thickness = 1.0

    @property
    def name(self):
        return 'Elastic Linear Material'

    @property
    def beam_thickness(self) -> float:
        return self._beam_thickness

    @beam_thickness.setter
    def beam_thickness(self, new_thickness: float):
        self._beam_thickness = new_thickness

    def get_elastic_matrix(self, plane_stress: bool = False) -> np.ndarray:
        if plane_stress:
            return self._get_plane_stress_matrix()
        else:
            return self._get_plane_strain_matrix()

    def _get_plane_stress_matrix(self) -> np.ndarray:
        poisson = self.poisson_ratio
        young = self.young_modulus
        factor = young / (1 - poisson ** 2)
        matrix = np.array([[1, poisson, 0.],
                           [poisson, 1., 0.],
                           [0., 0., (1. - poisson) / 2]])
        return factor * matrix

    def _get_plane_strain_matrix(self) -> np.ndarray:
        poisson = self.poisson_ratio
        young = self.young_modulus
        factor = young / ((1 + poisson) * (1 - 2 * poisson))
        matrix = np.array([[1 - poisson, poisson, 0.],
                           [poisson, 1 - poisson, 0.],
                           [0., 0., (1 - 2 * poisson) / 2]])
        return factor * matrix
