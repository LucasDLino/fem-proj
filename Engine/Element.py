from typing import Optional, List
import numpy as np

from Engine.Gauss import Gauss
from Engine.Node import Node
from Engine.Material import Material


class Element(object):
    """
     Represents a finite element used in structural analysis.

     Attributes:
         nodes (List[Node]): List of nodes that define the element.

         material (Optional[Material]): Material assigned to the element.

         gauss (Gauss): Gauss quadrature method for numerical integration.

         elem_dofs (int): Number of degrees of freedom associated with the element.
     """

    def __init__(self, nodes: List[Node] = None, material: Material = Optional[Material]):
        """
       Initializes an Element object.

       Args:
           nodes (List[Node], optional): List of nodes that define the element. Defaults to None.
           material (Material, optional): Material assigned to the element. Defaults to None.
       """
        self.label = None

        if nodes is None:
            nodes = []
        self.nodes = nodes
        self.material = material
        self.gauss = Gauss()
        self.elem_dofs: int = 0

        # Element data
        self.stress_gp = None
        self.strain_gp = None

    @property
    def name(self):
        """Returns the name of the element."""
        return 'Element'

    @property
    def max_nodes(self):
        """Returns the maximum number of nodes the element can have."""
        return None

    def add_node(self, node: Node):
        """
        Adds a node to the element.

        Args:
            node (Node): Node to be added to the element.

        Raises:
            ValueError: If the maximum number of nodes is exceeded.
        """
        if self.max_nodes is not None and len(self.nodes) >= self.max_nodes:
            raise ValueError(f'{self.name} can only have {self.max_nodes} nodes')

        self.nodes.append(node)

    def set_material(self, material: Material):
        """
        Sets the material for the element.

        Args:
            material (Material): Material assigned to the element.
        """
        self.material = material

    def count_elem_dofs(self) -> int:
        """Counts the degrees of freedom associated with the element."""
        if self.elem_dofs == 0:
            self.elem_dofs = len(self.nodes) * 2
        return self.elem_dofs

    def get_number_gp(self, stiff_intgr_type: str) -> int:
        """Returns the number of gauss points for numerical integration."""
        raise NotImplementedError('Method get_number_gp not implemented')

    def shape_functions(self, xi: float, eta: float) -> np.ndarray:
        """" Computes the shape functions of the element."""
        raise NotImplementedError('Method shape_functions not implemented')

    def shape_functions_derivative(self, xi: float, eta: float) -> np.ndarray:
        """Computes the derivative of the shape functions."""
        raise NotImplementedError('Method shape_functions_derivative not implemented')

    def jacobian(self, derivative: np.ndarray) -> np.ndarray:
        """Computes the Jacobian matrix for the element."""
        raise NotImplementedError('Method jacobian not implemented')

    @staticmethod
    def jacobian_determinant(jacobian: np.ndarray) -> float:
        """Computes the determinant of the Jacobian matrix."""
        return np.linalg.det(jacobian)

    @staticmethod
    def inverse_jacobian(jacobian: np.ndarray) -> np.ndarray:
        """Computes the inverse of the Jacobian matrix."""
        return np.linalg.inv(jacobian)

    def compute_elem_stiffness_matrix(self, stiff_intgr_type: str) -> np.ndarray:
        """Computes the element stiffness matrix."""
        raise NotImplementedError('Method compute_elem_stiffness_matrix not implemented')

    def assemble_elem_b_matrix(self, shape_derivative: np.ndarray) -> np.ndarray:
        """Assembles the B matrix for the element."""
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
    def get_connectivity_vector(self) -> np.ndarray:
        """Returns the connectivity vector for global assembly."""
        steering = np.full(self.count_elem_dofs(), -1)
        for i, node in enumerate(self.nodes):
            if not node.is_constrained_x():
                steering[2 * i] = node.global_index_x
            if not node.is_constrained_y():
                steering[2 * i + 1] = node.global_index_y
        return steering

    def get_elem_displacement_from_global(self, global_displacement_vector: np.ndarray) -> np.ndarray:
        """Returns the element displacement vector from the global displacement vector."""
        steering = self.get_connectivity_vector()
        return np.array([global_displacement_vector[i] for i in steering])

    def max_size(self):
        """Computes the maximum size of the element."""
        x = [node.x for node in self.nodes]
        y = [node.y for node in self.nodes]

        # Calculate the maximum distance between any two nodes
        return max(max(x) - min(x), max(y) - min(y))

    def compute_stress_strain(self, global_displacement_vector: np.ndarray, stress_strain_intgr_type: str) -> (np.ndarray, np.ndarray):
        """Computes the stress and strain at the gauss points."""
        raise NotImplementedError('Method compute_stress_strain not implemented')

    def extrapolate_stress_strain_gp_to_nodes(self, stress_strain_intgr_type: str):
        """Extrapolates the stress or strain from the gauss points to the nodes."""
        raise NotImplementedError('Method extrapolate_stress_strain_gp_to_nodes not implemented')
