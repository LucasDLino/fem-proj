from typing import Optional, List
import numpy as np

from Engine.Gauss import Gauss
from Engine.Node import Node
from Engine.Material import Material


class Element(object):
    def __init__(self, nodes: List[Node] = None, material: Material = Optional[Material]):
        if nodes is None:
            nodes = []
        self.nodes = nodes
        self.material = material
        self.gauss = Gauss()
        self.elem_dofs = 0

    @property
    def name(self):
        return 'Element'

    @property
    def max_nodes(self):
        return None

    def add_node(self, node: Node):
        if self.max_nodes is not None and len(self.nodes) >= self.max_nodes:
            raise ValueError(f'{self.name} can only have {self.max_nodes} nodes')

        self.nodes.append(node)

    def set_material(self, material: Material):
        self.material = material

    def count_elem_dofs(self) -> int:
        if self.elem_dofs == 0:
            self.elem_dofs = len(self.nodes) * 2
        return self.elem_dofs

    def shape_functions(self, xi: float, eta: float) -> np.ndarray:
        raise NotImplementedError('Method shape_functions not implemented')

    def shape_functions_derivative(self, xi: float, eta: float) -> np.ndarray:
        raise NotImplementedError('Method shape_functions_derivative not implemented')

    def jacobian(self, derivative: np.ndarray) -> np.ndarray:
        raise NotImplementedError('Method jacobian not implemented')

    @staticmethod
    def jacobian_determinant(jacobian: np.ndarray) -> float:
        return np.linalg.det(jacobian)

    @staticmethod
    def inverse_jacobian(jacobian: np.ndarray) -> np.ndarray:
        return np.linalg.inv(jacobian)

    def compute_elem_stiffness_matrix(self, gauss_points: int) -> np.ndarray:
        raise NotImplementedError('Method compute_elem_stiffness_matrix not implemented')

    def assemble_elem_b_matrix(self, shape_derivative: np.ndarray):
        num_nodes = len(self.nodes)

        num_dofs = self.count_elem_dofs()
        b_matrix = np.zeros((3, num_dofs))

        for i in range(num_nodes):
            # Adjust index calculations to start from 0
            b_matrix[0, 2 * i] = shape_derivative[0, i]
            b_matrix[1, 2 * i + 1] = shape_derivative[1, i]
            b_matrix[2, 2 * i] = shape_derivative[1, i]
            b_matrix[2, 2 * i + 1] = shape_derivative[0, i]

        return b_matrix

    # This vector is used to assemble the global stiffness matrix
    def get_steering_vector(self):
        steering = np.full(self.count_elem_dofs(), -1)
        for i, node in enumerate(self.nodes):
            if not node.is_constrained_x():
                steering[2 * i] = node.global_index_x
            if not node.is_constrained_y():
                steering[2 * i + 1] = node.global_index_y
        return steering

    def max_size(self):
        x = [node.x for node in self.nodes]
        y = [node.y for node in self.nodes]

        # Calculate the maximum distance between any two nodes
        return max(max(x) - min(x), max(y) - min(y))
