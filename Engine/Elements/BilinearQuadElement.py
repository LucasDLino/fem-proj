from typing import List, Optional
import numpy as np

from Engine.Element import Element
from Engine.Material import Material
from Engine.Materials.LinearElasticMaterial import LinearElasticMaterial
from Engine.Node import Node


class BilinearQuadElement(Element):
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
        return 0.25 * np.array([[(1. - xi) * (1. - eta)],  # N1 (bottom left)
                                [(1. + xi) * (1. - eta)],  # N2 (bottom right)
                                [(1. + xi) * (1. + eta)],  # N3 (top right)
                                [(1. - xi) * (1. + eta)]])  # N4 (top left)

    def shape_functions_derivative(self, xi: float, eta: float) -> np.ndarray:
        return 0.25 * np.array([[-(1. - eta), (1. - eta), (1. + eta), -(1. + eta)],  # dN1/dxi, dN2/dxi, dN3/dxi, dN4/dxi
                                [-(1. - xi), -(1. + xi), (1. + xi), (1. - xi)]])  # dN1/deta, dN2/deta, dN3/deta, dN4/deta

    def jacobian(self, derivative: np.ndarray) -> np.ndarray:
        x = np.array([node.x for node in self.nodes])
        y = np.array([node.y for node in self.nodes])

        return derivative @ np.array([x, y]).T

    def compute_elem_stiffness_matrix(self, number_gp: int) -> np.ndarray:
        stiffness = np.zeros((self.count_elem_dofs(), self.count_elem_dofs()))

        weights = self.gauss.get_weights(number_gp)

        for i, weight in enumerate(weights):

            wi = weights[i]

            points = self.gauss.get_points(number_gp)

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

    def compute_stress_strain(self, global_displacement_vector: np.ndarray, number_gp: int) -> (np.ndarray, np.ndarray):
        """Implementation in BilinearQuadElement to compute stress and strain at the gauss points and nodes."""

        self.stress_gp = []
        self.strain_gp = []

        arranged_gauss_points = self.gauss.get_ordered_points(number_gp)

        # Compute the stress and strain at the gauss points in ordered manner
        for i in range(len(arranged_gauss_points)):
            xi, eta = arranged_gauss_points[i]
            shape_derivative = self.shape_functions_derivative(xi, eta)
            jacobian = self.jacobian(shape_derivative)
            inverse_jacobian = self.inverse_jacobian(jacobian)

            derivative = inverse_jacobian @ shape_derivative

            b_matrix = self.assemble_elem_b_matrix(derivative)

            # Compute the element displacement vector from the global displacement vector
            elem_displacement_vector = self.get_elem_displacement_from_global(global_displacement_vector)

            # Compute the strain
            strain = b_matrix @ elem_displacement_vector

            # Compute the stress
            elastic_matrix = self.material.get_elastic_matrix(True)
            stress = elastic_matrix @ strain

            # Store the stress and strain at the gauss points
            self.stress_gp.append(stress)
            self.strain_gp.append(strain)

        # Convert the lists to numpy arrays
        self.stress_gp = np.array(self.stress_gp)  # each row corresponds to a gauss point and each column to a stress component
        self.strain_gp = np.array(self.strain_gp)  # each row corresponds to a gauss point and each column to a strain component

        return self.stress_gp, self.strain_gp

    def construct_extrapolation_matrix_2gp(self) -> np.ndarray:
        """Constructs the extrapolation matrix for the element."""
        num_nodes = len(self.nodes)

        # Construct parametric coordinates
        parametric_coords = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])

        num_rows = len(parametric_coords)

        extrapolation_matrix = np.zeros((num_rows, num_nodes))

        # We will evaluate the shape functions at the parametric coordinates and populate the extrapolation matrix
        for i in range(num_rows):
            xi = parametric_coords[i, 0]
            eta = parametric_coords[i, 1]

            # N_i = 0.25 * (1 +- xi') * (1 +- eta') in which xi' = xi * sqrt(3) and eta' = eta * sqrt(3)

            shape_funcs = self.shape_functions(xi * np.sqrt(3), eta * np.sqrt(3))

            extrapolation_matrix[i, :] = shape_funcs.ravel()

        return extrapolation_matrix

    def extrapolate_stress_strain_gp_to_nodes(self, number_gp: int):
        """Extrapolates the stress or strain from the gauss points to the nodes."""

        if number_gp == 2:  # Each row corresponds to a gauss point and each column to a node
            extrapolation_matrix = self.construct_extrapolation_matrix_2gp()

            # Extrapolate the stress and strain from the gauss points to the nodes
            strain_xx = extrapolation_matrix @ self.strain_gp[:, 0]
            strain_yy = extrapolation_matrix @ self.strain_gp[:, 1]
            strain_xy = extrapolation_matrix @ self.strain_gp[:, 2]

            stress_xx = extrapolation_matrix @ self.stress_gp[:, 0]
            stress_yy = extrapolation_matrix @ self.stress_gp[:, 1]
            stress_xy = extrapolation_matrix @ self.stress_gp[:, 2]

            # Put the extrapolated values in the correct nodes
            for i, node in enumerate(self.nodes):
                # node.strain corresponds to a list of lists of type [[elem_label, (nparray) strain], ...]
                node.strain.append([self.label, np.array([strain_xx[i], strain_yy[i], strain_xy[i]])])
                node.stress.append([self.label, np.array([stress_xx[i], stress_yy[i], stress_xy[i]])])

        elif number_gp == 1:
            for i, node in enumerate(self.nodes):
                node.strain.append([self.label, self.strain_gp[0]])
                node.stress.append([self.label, np.array(self.stress_gp[0][0:3])])
        else:
            raise NotImplementedError('Method extrapolate_stress_strain_gp_to_nodes not implemented')
