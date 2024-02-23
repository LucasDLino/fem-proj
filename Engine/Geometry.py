from typing import List
import numpy as np

from Engine.Material import Material
from Engine.Node import Node
from Engine.Element import Element
from Engine.Elements.BilinearQuadElement import BilinearQuadElement
from Engine.Elements.QuadraticQuadElement import QuadraticQuadElement


class Geometry(object):
    def __init__(self):
        self.nodes = []
        self.elements = []
        self.global_free_dofs: int = 0

    def __str__(self):
        return f'Geometry with {len(self.nodes)} nodes and {len(self.elements)} elements'

    def add_node(self, x: float, y: float) -> Node:
        self.nodes.append(Node(x, y))
        # Set node label
        self.nodes[-1].label = len(self.nodes)
        return self.nodes[-1]

    def add_bilinear_quadrilateral_element(self, nodes: List[Node]) -> Element:
        self.elements.append(BilinearQuadElement(nodes))
        return self.elements[-1]

    def add_quadratic_quadrilateral_element(self, nodes: List[Node]) -> Element:
        self.elements.append(QuadraticQuadElement(nodes))
        return self.elements[-1]

    def set_all_materials(self, material: Material):
        for element in self.elements:
            element.set_material(material)

    def count_global_free_dofs(self) -> int:
        if self.global_free_dofs == 0:
            for node in self.nodes:
                if not node.is_constrained_x():
                    self.global_free_dofs += 1
                if not node.is_constrained_y():
                    self.global_free_dofs += 1
        return self.global_free_dofs

    def compute_nodal_global_indices(self):
        global_index_count = 0
        for node in self.nodes:
            if not node.is_constrained_x():
                node.set_global_index_x(global_index_count)
                global_index_count += 1
            if not node.is_constrained_y():
                node.set_global_index_y(global_index_count)
                global_index_count += 1

    def assemble_global_forces_vector(self) -> np.ndarray:
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
        elem_dofs = element.count_elem_dofs()
        g = element.get_connectivity_vector()
        for i in range(elem_dofs):
            if g[i] != -1:
                for j in range(elem_dofs):
                    if g[j] != -1:
                        global_stiffness_matrix[g[i], g[j]] += element_stiffness_matrix[i, j]
        return global_stiffness_matrix
