from typing import List
import numpy as np

from Engine.Material import Material
from Engine.Node import Node
from Engine.Element import Element
from Engine.Elements.BilinearQuadElement import BilinearQuadElement
from Engine.Elements.QuadraticQuadElement import QuadraticQuadElement


class Geometry(object):
    """
    Represents the geometry of a finite element structure.

    Attributes:
        nodes (List[Node]): List of nodes in the geometry.

        elements (List[Element]): List of elements in the geometry.

        global_free_dofs (int): Number of global free degrees of freedom.
    """

    def __init__(self):
        """Initializes a Geometry object."""
        self.nodes = []
        self.elements = []
        self.global_free_dofs: int = 0

    def __str__(self):
        """Returns a string representation of the geometry."""
        return f'Geometry with {len(self.nodes)} nodes and {len(self.elements)} elements'

    def add_node(self, x: float, y: float) -> Node:
        """
        Adds a node to the geometry.

        Args:
            x (float): X-coordinate of the node.

            y (float): Y-coordinate of the node.

        Returns:
            Node: The newly added node.
        """
        self.nodes.append(Node(x, y))
        # Set node label
        self.nodes[-1].label = len(self.nodes)
        return self.nodes[-1]

    def add_element(self, nodes: List[Node]) -> Element:
        """
        Adds an element to the geometry.

        Args:
            nodes (List[Node]): List of nodes defining the element.

        Returns:
            Element: The newly added element.

        Raises:
            ValueError: If the element type is not supported.
        """
        if len(nodes) == 4:
            return self.add_bilinear_quadrilateral_element(nodes)
        elif len(nodes) == 8:
            return self.add_quadratic_quadrilateral_element(nodes)
        else:
            raise ValueError('Element type not supported')

    def add_bilinear_quadrilateral_element(self, nodes: List[Node]) -> Element:
        """
        Adds a bilinear quadrilateral element to the geometry.

        Args:
            nodes (List[Node]): List of nodes defining the element.

        Returns:
            Element: The newly added bilinear quadrilateral element.
        """
        self.elements.append(BilinearQuadElement(nodes))
        # Set element label
        self.elements[-1].label = len(self.elements)
        return self.elements[-1]

    def add_quadratic_quadrilateral_element(self, nodes: List[Node]) -> Element:
        """
        Adds a quadratic quadrilateral element to the geometry.

        Args:
            nodes (List[Node]): List of nodes defining the element.

        Returns:
            Element: The newly added quadratic quadrilateral element.
        """
        self.elements.append(QuadraticQuadElement(nodes))
        # Set element label
        self.elements[-1].label = len(self.elements)
        return self.elements[-1]

    def set_all_materials(self, material: Material):
        """
        Sets the material for all elements in the geometry.

        Args:
            material (Material): Material to be assigned to the elements.
        """
        for element in self.elements:
            element.set_material(material)

    def count_global_free_dofs(self) -> int:
        """
        Counts the number of global free degrees of freedom in the geometry.

        Returns:
            int: Number of global free degrees of freedom.
        """
        if self.global_free_dofs == 0:
            for node in self.nodes:
                if not node.is_constrained_x():
                    self.global_free_dofs += 1
                if not node.is_constrained_y():
                    self.global_free_dofs += 1
        return self.global_free_dofs

    def compute_nodal_global_indices(self):
        """Computes global indices for all nodes in the geometry."""
        global_index_count = 0
        for node in self.nodes:
            if not node.is_constrained_x():
                node.set_global_index_x(global_index_count)
                global_index_count += 1
            if not node.is_constrained_y():
                node.set_global_index_y(global_index_count)
                global_index_count += 1

    def assemble_global_forces_vector(self) -> np.ndarray:
        """
        Assembles the global forces vector for the geometry.

        Returns:
            np.ndarray: Global forces vector.
        """
        forces = np.zeros((self.count_global_free_dofs(), 1))
        global_index_count = 0
        for node in self.nodes:
            if not node.is_constrained_x():
                forces[global_index_count] = node.x_load
                global_index_count += 1
            if not node.is_constrained_y():
                forces[global_index_count] = node.y_load
                global_index_count += 1
        return forces

    @staticmethod
    def assemble_global_stiffness_matrix(global_stiffness_matrix: np.ndarray, element_stiffness_matrix: np.ndarray, element: Element) -> np.ndarray:
        """
        Assembles the global stiffness matrix.

        Args:
            global_stiffness_matrix (np.ndarray): Global stiffness matrix.

            element_stiffness_matrix (np.ndarray): Element stiffness matrix.

            element (Element): Element for which stiffness matrix is assembled.

        Returns:
            np.ndarray: Updated global stiffness matrix.
        """
        elem_dofs = element.count_elem_dofs()
        g = element.get_connectivity_vector()
        for i in range(elem_dofs):
            if g[i] != -1:
                for j in range(elem_dofs):
                    if g[j] != -1:
                        global_stiffness_matrix[g[i], g[j]] += element_stiffness_matrix[i, j]
        return global_stiffness_matrix
