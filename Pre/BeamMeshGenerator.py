from typing import Optional

from Engine.Geometry import Geometry


class BeamMeshGenerator:
    def __init__(self, geometry: Geometry):
        self.geometry = geometry

    def generate_bilinear_mesh(self, width: float, height: float, num_x_nodes: int, num_y_nodes: int, x_origin: Optional[float] = 0., y_origin: Optional[float] = 0.):
        x_spacing = width / (num_x_nodes - 1)
        y_spacing = height / (num_y_nodes - 1)

        for i in range(num_x_nodes):
            for j in range(num_y_nodes):
                x = x_origin + i * x_spacing
                y = y_origin + j * y_spacing
                self.geometry.add_node(x, y)

        for i in range(num_x_nodes - 1):
            for j in range(num_y_nodes - 1):
                n1 = j + i * num_y_nodes
                n2 = j + (i + 1) * num_y_nodes
                n3 = n1 + 1
                n4 = n2 + 1
                self.geometry.add_bilinear_quadrilateral_element([self.geometry.nodes[n1],
                                                                  self.geometry.nodes[n2],
                                                                  self.geometry.nodes[n4],
                                                                  self.geometry.nodes[n3]])

    def generate_quadratic_mesh(self, width: float, height: float, num_x_nodes: int, num_y_nodes: int, x_origin: Optional[float] = 0., y_origin: Optional[float] = 0.):
        pass
