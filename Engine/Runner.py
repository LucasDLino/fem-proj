from typing import Optional

from Engine.Geometry import Geometry
from Engine.Materials.LinearElasticMaterial import LinearElasticMaterial
from Pos.Visualizer import Visualizer
import numpy as np


class Runner(object):
    def __init__(self):
        # Geometry
        self.geometry = Geometry()
        self.count_free_dofs = None

        # Global matrices
        self.global_stiffness_matrix = None
        self.global_force_vector = None
        self.global_displacement_vector = None

        # Analysis parameters
        self._number_gp: int = 2

    @property
    def name(self):
        return 'Engine'

    @property
    def number_gp(self):
        return self._number_gp

    @number_gp.setter
    def number_gp(self, value: int):
        if value < 1:
            raise ValueError('Number of Gauss points must be greater than 0')
        elif value > 4:
            raise ValueError('Number of Gauss points must be less than 5')
        self._number_gp = value

    def __str__(self):
        return f'Engine with {len(self.geometry.nodes)} nodes and {len(self.geometry.elements)} elements'

    def construct_beam_geometry(self, nodes, elements_connectivity):
        # Define node coordinates from geom

        for node_id, (x, y) in nodes.items():
            nodes[node_id] = self.geometry.add_node(x, y)

        # Create elements
        for connec in elements_connectivity:
            node_ids = [nodes[str(node_id)] for node_id in connec]
            self.geometry.add_element(node_ids)




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

    def run_analysis(self):
        # Compute nodal global indices for each node
        self.geometry.compute_nodal_global_indices()

        # Perform the analysis
        self.global_stiffness_matrix = self.integrate_and_assemble_stiffness_matrix()
        self.global_force_vector = self.geometry.assemble_global_forces_vector()
        self.global_displacement_vector = self.solve_displacements()

        # Compute the stress and strain at the gauss points for each element and extrapolate to the nodes
        self.compute_elements_stress_strain()
        self.average_nodal_stress_strain()

    def integrate_and_assemble_stiffness_matrix(self):
        self.global_stiffness_matrix = np.zeros((self.geometry.count_global_free_dofs(), self.geometry.count_global_free_dofs()))

        for element in self.geometry.elements:
            element_stiffness_matrix = element.compute_elem_stiffness_matrix(self._number_gp)
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

    def compute_elements_stress_strain(self):
        for element in self.geometry.elements:
            # Compute the stress and strain at the gauss points
            element.compute_stress_strain(self.global_displacement_vector, self.number_gp)
            element.extrapolate_stress_strain_gp_to_nodes(1)

    def average_nodal_stress_strain(self):

        for node in self.geometry.nodes:
            node.stress_avg = np.zeros(3)
            node.strain_avg = np.zeros(3)

            # Loop over each stress and strain that has the format [[elem_label, (nparray) strain], ...]
            for i in range(len(node.stress)):
                # Print all elements contributing to the node stress
                # print(f'Node {node.label} stress from element {node.stress[i][0]}: {node.stress[i][1]}')
                node.stress_avg += node.stress[i][1]

            for i in range(len(node.strain)):
                # Print all elements contributing to the node strain
                # print(f'Node {node.label} strain from element {node.strain[i][0]}: {node.strain[i][1]}')
                node.strain_avg += node.strain[i][1]

            node.stress_avg /= len(node.stress)
            node.strain_avg /= len(node.strain)

    def show_results(self):
        visualization = Visualizer(self.geometry.nodes, self.geometry.elements)

        visualization.visualize_undeformed_geometry()
        visualization.visualize_deformed_geometry(self.global_displacement_vector, 1000, add_nodal_forces=True)
        # visualization.visualize_disp_table(self.global_displacement_vector)

        visualization.visualize_nodal_stress("xx")
        # visualization.visualize_nodal_stress("yy")
        # visualization.visualize_nodal_stress("xy")

        visualization.visualize_nodal_strain("yy")

        visualization.visualize_displacement(self.global_displacement_vector, "x")
        # visualization.visualize_displacement(self.global_displacement_vector, "y")
