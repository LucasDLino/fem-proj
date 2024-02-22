from typing import List
import numpy as np

from Engine.Material import Material
from Engine.Node import Node
from Engine.Element import Element
from Engine.Elements.BilinearQuadrilateralElement import BilinearQuadrilateralElement
from Engine.Elements.QuadraticQuadrilateralElement import QuadraticQuadrilateralElement


class Geometry(object):
    def __init__(self):
        self.nodes = []
        self.elements = []
        self.count_free_dofs: int = 0
        self.boundary_conditions_matrix: np.ndarray = None

    def __str__(self):
        return f'Geometry with {len(self.nodes)} nodes and {len(self.elements)} elements'

    def add_node(self, x: float, y: float) -> Node:
        self.nodes.append(Node(x, y))
        return self.nodes[-1]

    def add_bilinear_quadrilateral_element(self, nodes: List[Node]) -> Element:
        self.elements.append(BilinearQuadrilateralElement(nodes))
        return self.elements[-1]

    def add_quadratic_quadrilateral_element(self, nodes: List[Node]) -> Element:
        self.elements.append(QuadraticQuadrilateralElement(nodes))
        return self.elements[-1]

    def set_all_materials(self, material: Material):
        for element in self.elements:
            element.set_material(material)

    def free_dofs(self) -> int:
        if self.count_free_dofs == 0:
            for node in self.nodes:
                if not node.is_constrained_x():
                    self.count_free_dofs += 1
                if not node.is_constrained_y():
                    self.count_free_dofs += 1
        return self.count_free_dofs

    # def get_nodal_loads_matrix(self) -> np.ndarray:
    #     loads = np.zeros((len(self.nodes), 2))
    #     for i, node in enumerate(self.nodes):
    #         loads[i, 0] = node.x_load
    #         loads[i, 1] = node.y_load
    #     return loads

    def get_free_dofs_matrix(self) -> np.ndarray:
        free_dofs_matrix = np.ones(self.free_dofs(), 2)

        count_free_dofs = 0

        for i, node in enumerate(self.nodes):
            if node.is_constrained_x():
                free_dofs_matrix[i, 0] = 0
            if node.is_constrained_y():
                free_dofs_matrix[i, 1] = 0

        for i, node in enumerate(self.nodes):
            if free_dofs_matrix[i, 0] != 0:
                free_dofs_matrix[i, 0] = count_free_dofs
                count_free_dofs += 1
            if free_dofs_matrix[i, 1] != 0:
                free_dofs_matrix[i, 1] = count_free_dofs
                count_free_dofs += 1

        return free_dofs_matrix

    def get_boundary_conditions_matrix(self) -> np.ndarray:
        if self.boundary_conditions_matrix is None:
            self.boundary_conditions_matrix = np.zeros(len(self.nodes) * 2)
            for i, node in enumerate(self.nodes):
                if node.is_constrained_x():
                    self.boundary_conditions_matrix[i * 2] = 1
                if node.is_constrained_y():
                    self.boundary_conditions_matrix[i * 2 + 1] = 1
        return self.boundary_conditions_matrix

    def assemble_global_forces_vector(self) -> np.ndarray:
        forces = np.zeros(self.free_dofs())
        for i, node in enumerate(self.nodes):
            if not node.is_constrained_x():
                forces[i] = node.x_load
            if not node.is_constrained_y():
                forces[i + 1] = node.y_load
        return forces

    def assemble_global_stiffness_matrix(self, global_stiffness_matrix: np.ndarray, element_stiffness_matrix: np.ndarray, element: Element) -> np.ndarray:
        # TODO: Check this method
        # Here I have to check if the degrees of freedom are constrained and then assemble the global stiffness matrix
        for (i, node) in enumerate(element.nodes):
            if not node.is_constrained_x() and not node.is_constrained_y():
                global_stiffness_matrix[i:i + 2, i:i + 2] += element_stiffness_matrix[i:i + 2, i:i + 2]
