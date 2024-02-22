from typing import Optional

from Engine.Geometry import Geometry
from Engine.Materials.LinearElasticMaterial import LinearElasticMaterial
from Pos.Visualizer import Visualizer
import numpy as np


class Engine(object):
    def __init__(self):
        # Geometry
        self.geometry = Geometry()
        self.count_free_dofs = None

        # Global matrices
        self.global_stiffness_matrix = None
        self.global_force_vector = None
        self.global_displacement_vector = None

        # Analysis parameters
        self.gauss_points: int = 2

    @property
    def name(self):
        return 'Engine'

    def __str__(self):
        return f'Engine with {len(self.geometry.nodes)} nodes and {len(self.geometry.elements)} elements'

    def construct_beam_geometry(self):
        # Create beam nodes
        n1 = self.geometry.add_node(0., -10.)
        n2 = self.geometry.add_node(0., 0.)
        n3 = self.geometry.add_node(0., 10.)
        n4 = self.geometry.add_node(10., -10.)
        n5 = self.geometry.add_node(10., 0.)
        n6 = self.geometry.add_node(10., 10.)
        n7 = self.geometry.add_node(20., -10.)
        n8 = self.geometry.add_node(20., 0.)
        n9 = self.geometry.add_node(20., 10.)
        n10 = self.geometry.add_node(30., -10.)
        n11 = self.geometry.add_node(30., 0.)
        n12 = self.geometry.add_node(30., 10.)
        n13 = self.geometry.add_node(40., -10.)
        n14 = self.geometry.add_node(40., 0.)
        n15 = self.geometry.add_node(40., 10.)
        n16 = self.geometry.add_node(50., -10.)
        n17 = self.geometry.add_node(50., 0.)
        n18 = self.geometry.add_node(50., 10.)
        n19 = self.geometry.add_node(60., -10.)
        n20 = self.geometry.add_node(60., 0.)
        n21 = self.geometry.add_node(60., 10.)

        # Compute nodal global indices for each node
        self.geometry.compute_nodal_global_indices()

        # Create beam elements
        self.geometry.add_bilinear_quadrilateral_element([n1, n4, n5, n2])
        self.geometry.add_bilinear_quadrilateral_element([n2, n5, n6, n3])
        self.geometry.add_bilinear_quadrilateral_element([n4, n7, n8, n5])
        self.geometry.add_bilinear_quadrilateral_element([n5, n8, n9, n6])
        self.geometry.add_bilinear_quadrilateral_element([n7, n10, n11, n8])
        self.geometry.add_bilinear_quadrilateral_element([n8, n11, n12, n9])
        self.geometry.add_bilinear_quadrilateral_element([n10, n13, n14, n11])
        self.geometry.add_bilinear_quadrilateral_element([n11, n14, n15, n12])
        self.geometry.add_bilinear_quadrilateral_element([n13, n16, n17, n14])
        self.geometry.add_bilinear_quadrilateral_element([n14, n17, n18, n15])
        self.geometry.add_bilinear_quadrilateral_element([n16, n19, n20, n17])
        self.geometry.add_bilinear_quadrilateral_element([n17, n20, n21, n18])

    def set_linear_elastic_material(self, young_modulus: float, poisson_ratio: float, thickness: Optional[float] = None):
        # Set material
        linear_material = LinearElasticMaterial(young_modulus, poisson_ratio)
        if thickness is not None:
            linear_material.beam_thickness = thickness
        self.geometry.set_all_materials(linear_material)

    def set_boundary_conditions(self, node: int, x: bool, y: bool):
        self.geometry.nodes[node].constrain(x, y)

    def apply_nodal_load(self, node: int, x: float, y: float):
        self.geometry.nodes[node].apply_load(x, y)

    def integrate_and_assemble_stiffness_matrix(self):
        self.global_stiffness_matrix = np.zeros((self.geometry.count_global_free_dofs(), self.geometry.count_global_free_dofs()))

        for element in self.geometry.elements:
            element_stiffness_matrix = element.compute_elem_stiffness_matrix(self.gauss_points)
            self.global_stiffness_matrix = self.geometry.assemble_global_stiffness_matrix(self.global_stiffness_matrix, element_stiffness_matrix, element)

        return self.global_stiffness_matrix

    def solve_displacements(self):
        self.global_displacement_vector = np.zeros(len(self.geometry.nodes) * 2)
        # numpy division of matrices
        displacements = np.linalg.solve(self.global_stiffness_matrix, self.global_force_vector)

        # Assemble the global displacement vector
        for i, node in enumerate(self.geometry.nodes):
            if not node.is_constrained_x():
                self.global_displacement_vector[node.global_index_x] = displacements[node.global_index_x]
            if not node.is_constrained_y():
                self.global_displacement_vector[node.global_index_y] = displacements[node.global_index_y]

        return self.global_displacement_vector

    def run_analysis(self):
        self.global_stiffness_matrix = self.integrate_and_assemble_stiffness_matrix()
        self.global_force_vector = self.geometry.assemble_global_forces_vector()
        self.global_displacement_vector = self.solve_displacements()

    def show_results(self):
        # print nodes
        # print('Nodes:')
        # for i, node in enumerate(self.geometry.nodes):
        #     print(f'Node {i + 1}: x = {node.x}, y = {node.y} - Constrained x: {node.is_constrained_x()}, Constrained y: {node.is_constrained_y()}')

        # print global force vector
        # print('Global force vector:')
        # print(self.global_force_vector)

        # print global displacement results
        # print('Global displacement results:')
        # for i, node in enumerate(self.geometry.nodes):
        #     print(f'Node {i + 1}: u = {self.global_displacement_vector[i * 2]}, v = {self.global_displacement_vector[i * 2 + 1]} with coordinates {node.x}, {node.y}')

        visualization = Visualizer(self.geometry.nodes, self.geometry.elements)

        visualization.visualize_undeformed_geometry()
        visualization.visualize_deformed_geometry(self.global_displacement_vector, 100, add_nodal_forces=True)
        visualization.visualize_disp_table(self.global_displacement_vector)
