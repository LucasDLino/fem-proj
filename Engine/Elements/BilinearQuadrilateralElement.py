from typing import List, Optional
import numpy as np

from Engine.Element import Element
from Engine.Material import Material
from Engine.Materials.LinearElasticMaterial import LinearElasticMaterial
from Engine.Node import Node


class BilinearQuadrilateralElement(Element):
    def __init__(self, nodes: List[Node] = None, material: Material = Optional[Material]):
        super().__init__(nodes, material)

    @property
    def name(self):
        return 'Bilinear Quadrilateral Element'

    @property
    def max_nodes(self):
        return 4

    def get_thickness(self) -> float:
        if isinstance(self.material, LinearElasticMaterial):
            return self.material.beam_thickness
        else:
            raise ValueError('Material is not a LinearElasticMaterial')

    def count_elem_dofs(self) -> int:
        return len(self.nodes) * 2

    def shape_functions(self, xi: float, eta: float) -> np.ndarray:
        return 0.25 * np.array([[(1. - xi) * (1. - eta)],
                                [(1. + xi) * (1. - eta)],
                                [(1. + xi) * (1. + eta)],
                                [(1. - xi) * (1. + eta)]])

    def shape_functions_derivative(self, xi: float, eta: float) -> np.ndarray:
        return 0.25 * np.array([[-(1. - eta), (1. - eta), (1. + eta), -(1. + eta)],
                                [-(1. - xi), -(1. + xi), (1. + xi), (1. - xi)]])

    def jacobian(self, derivative: np.ndarray) -> np.ndarray:
        x = np.array([node.x for node in self.nodes])
        y = np.array([node.y for node in self.nodes])

        return derivative @ np.array([x, y]).T

    def compute_elem_stiffness_matrix(self, gauss_points: int) -> np.ndarray:
        stiffness = np.zeros((self.count_elem_dofs(), self.count_elem_dofs()))

        weights = self.gauss.get_weights(gauss_points)

        for i, weight in enumerate(weights):

            wi = weights[i]

            points = self.gauss.get_points(gauss_points)

            for j, point in enumerate(points):
                wj = weights[j]

                shape_derivative = self.shape_functions_derivative(points[i], points[j])

                jacobian = self.jacobian(shape_derivative)
                jacobian_determinant = self.jacobian_determinant(jacobian)
                inverse_jacobian = self.inverse_jacobian(jacobian)

                derivative = inverse_jacobian @ shape_derivative

                elastic_matrix = self.material.get_elastic_matrix(True)  # True for plane stress

                thickness = self.get_thickness()

                b_matrix = self.assemble_elem_b_matrix(derivative)

                stiffness += jacobian_determinant * thickness * wi * wj * (b_matrix.T @ elastic_matrix @ b_matrix)
        return stiffness
