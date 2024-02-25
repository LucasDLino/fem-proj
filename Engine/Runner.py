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

    def construct_beam_geometry(self):
        # Define node coordinates from geom
        node_coords = {
            1: (0., 0.),
            2: (0., 50.),
            3: (0., 100.),
            4: (0., 150.),
            5: (0., 200.),
            6: (0., 250.),
            7: (0., 300.),
            8: (0., 350.),
            9: (0., 400.),
            10: (50., 0.),
            11: (50., 100.),
            12: (50., 200.),
            13: (50., 300.),
            14: (50., 400.),
            15: (100., 0.),
            16: (100., 50.),
            17: (100., 100.),
            18: (100., 150.),
            19: (100., 200.),
            20: (100., 250.),
            21: (100., 300.),
            22: (100., 350.),
            23: (100., 400.),
            24: (150., 0.),
            25: (150., 100.),
            26: (150., 200.),
            27: (150., 300.),
            28: (150., 400.),
            29: (200., 0.),
            30: (200., 50.),
            31: (200., 100.),
            32: (200., 150.),
            33: (200., 200.),
            34: (200., 250.),
            35: (200., 300.),
            36: (200., 350.),
            37: (200., 400.),
            38: (250., 0.),
            39: (250., 100.),
            40: (250., 200.),
            41: (250., 300.),
            42: (250., 400.),
            43: (300., 0.),
            44: (300., 50.),
            45: (300., 100.),
            46: (300., 150.),
            47: (300., 200.),
            48: (300., 250.),
            49: (300., 300.),
            50: (300., 350.),
            51: (300., 400.),
            52: (350., 0.),
            53: (350., 100.),
            54: (350., 200.),
            55: (350., 300.),
            56: (350., 400.),
            57: (400., 0.),
            58: (400., 50.),
            59: (400., 100.),
            60: (400., 150.),
            61: (400., 200.),
            62: (400., 250.),
            63: (400., 300.),
            64: (400., 350.),
            65: (400., 400.),
            66: (450., 0.),
            67: (450., 100.),
            68: (450., 200.),
            69: (450., 300.),
            70: (450., 400.),
            71: (500., 0.),
            72: (500., 50.),
            73: (500., 100.),
            74: (500., 150.),
            75: (500., 200.),
            76: (500., 250.),
            77: (500., 300.),
            78: (500., 350.),
            79: (500., 400.),
            80: (550., 0.),
            81: (550., 100.),
            82: (550., 200.),
            83: (550., 300.),
            84: (550., 400.),
            85: (600., 0.),
            86: (600., 50.),
            87: (600., 100.),
            88: (600., 150.),
            89: (600., 200.),
            90: (600., 250.),
            91: (600., 300.),
            92: (600., 350.),
            93: (600., 400.),
            94: (650., 0.),
            95: (650., 100.),
            96: (650., 200.),
            97: (650., 300.),
            98: (650., 400.),
            99: (700., 0.),
            100: (700., 50.),
            101: (700., 100.),
            102: (700., 150.),
            103: (700., 200.),
            104: (700., 250.),
            105: (700., 300.),
            106: (700., 350.),
            107: (700., 400.),
            108: (750., 0.),
            109: (750., 100.),
            110: (750., 200.),
            111: (750., 300.),
            112: (750., 400.),
            113: (800., 0.),
            114: (800., 50.),
            115: (800., 100.),
            116: (800., 150.),
            117: (800., 200.),
            118: (800., 250.),
            119: (800., 300.),
            120: (800., 350.),
            121: (800., 400.)
        }

        # Create nodes
        nodes = {}
        for node_id, (x, y) in node_coords.items():
            nodes[node_id] = self.geometry.add_node(x, y)

        # Define element connectivity from connec
        element_connec = [
            [1, 10, 15, 16, 17, 11, 3, 2],
            [3, 11, 17, 18, 19, 12, 5, 4],
            [5, 12, 19, 20, 21, 13, 7, 6],
            [7, 13, 21, 22, 23, 14, 9, 8],
            [15, 24, 29, 30, 31, 25, 17, 16],
            [17, 25, 31, 32, 33, 26, 19, 18],
            [19, 26, 33, 34, 35, 27, 21, 20],
            [21, 27, 35, 36, 37, 28, 23, 22],
            [29, 38, 43, 44, 45, 39, 31, 30],
            [31, 39, 45, 46, 47, 40, 33, 32],
            [33, 40, 47, 48, 49, 41, 35, 34],
            [35, 41, 49, 50, 51, 42, 37, 36],
            [43, 52, 57, 58, 59, 53, 45, 44],
            [45, 53, 59, 60, 61, 54, 47, 46],
            [47, 54, 61, 62, 63, 55, 49, 48],
            [49, 55, 63, 64, 65, 56, 51, 50],
            [57, 66, 71, 72, 73, 67, 59, 58],
            [59, 67, 73, 74, 75, 68, 61, 60],
            [61, 68, 75, 76, 77, 69, 63, 62],
            [63, 69, 77, 78, 79, 70, 65, 64],
            [71, 80, 85, 86, 87, 81, 73, 72],
            [73, 81, 87, 88, 89, 82, 75, 74],
            [75, 82, 89, 90, 91, 83, 77, 76],
            [77, 83, 91, 92, 93, 84, 79, 78],
            [85, 94, 99, 100, 101, 95, 87, 86],
            [87, 95, 101, 102, 103, 96, 89, 88],
            [89, 96, 103, 104, 105, 97, 91, 90],
            [91, 97, 105, 106, 107, 98, 93, 92],
            [99, 108, 113, 114, 115, 109, 101, 100],
            [101, 109, 115, 116, 117, 110, 103, 102],
            [103, 110, 117, 118, 119, 111, 105, 104],
            [105, 111, 119, 120, 121, 112, 107, 106]
        ]

        # Create elements
        for connec in element_connec:
            node_ids = [nodes[node_id] for node_id in connec]
            self.geometry.add_quadratic_quadrilateral_element(node_ids)

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
            element.compute_stress_strain(self.global_displacement_vector, 1)
            element.extrapolate_stress_strain_gp_to_nodes(1)

    def average_nodal_stress_strain(self):

        for node in self.geometry.nodes:
            node.stress_avg = np.zeros(3)
            node.strain_avg = np.zeros(3)

            # Loop over each stress and strain that has the format [[elem_label, (nparray) strain], ...]
            for i in range(len(node.stress)):
                # Print all elements contributing to the node stress
                print(f'Node {node.label} stress from element {node.stress[i][0]}: {node.stress[i][1]}')
                node.stress_avg += node.stress[i][1]

            for i in range(len(node.strain)):
                # Print all elements contributing to the node strain
                print(f'Node {node.label} strain from element {node.strain[i][0]}: {node.strain[i][1]}')
                node.strain_avg += node.strain[i][1]

            node.stress_avg /= len(node.stress)
            node.strain_avg /= len(node.strain)

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
        visualization.visualize_nodal_stress("xx")
        # visualization.visualize_nodal_strain()

        visualization.visualize_displacement(self.global_displacement_vector, "y")
