from typing import Optional

from Engine.Geometry import Geometry


class BeamMeshGenerator:
    def __init__(self, geometry: Geometry):
        self.geometry = geometry

    from typing import Optional

    def generate_bilinear_mesh(self, width: float, height: float, num_elements_x: int, num_elements_y: int, x_origin: Optional[float] = 0., y_origin: Optional[float] = 0.):
        num_x_nodes = num_elements_x + 1
        num_y_nodes = num_elements_y + 1

        x_spacing = width / num_elements_x
        y_spacing = height / num_elements_y

        for i in range(num_x_nodes):
            for j in range(num_y_nodes):
                x = x_origin + i * x_spacing
                y = y_origin + j * y_spacing
                self.geometry.add_node(x, y)

        for i in range(num_elements_x):
            for j in range(num_elements_y):
                n1 = j + i * num_y_nodes
                n2 = j + (i + 1) * num_y_nodes
                n3 = n1 + 1
                n4 = n2 + 1
                self.geometry.add_element([self.geometry.nodes[n1],
                                           self.geometry.nodes[n2],
                                           self.geometry.nodes[n4],
                                           self.geometry.nodes[n3]])

    def generate_biquadratic_mesh(self, width: float, height: float, num_elements_x: int, num_elements_y: int, x_origin: Optional[float] = 0., y_origin: Optional[float] = 0.):
        num_rows = 2 * num_elements_x + 1
        num_columns = 2 * num_elements_y + 1

        x_spacing = width / (2 * num_elements_x)
        y_spacing = height / (2 * num_elements_y)

        for column in range(num_rows):
            for row in range(num_columns):
                if column % 2 == 0 or row % 2 == 0:
                    x = x_origin + column * x_spacing
                    y = y_origin + row * y_spacing
                    self.geometry.add_node(x, y)

        a = self.geometry.nodes
        for row in range(num_elements_y):
            for column in range(num_elements_x):
                n1 = column * (2 * num_elements_y + 1) + column * (num_elements_y + 1) + 2 * row
                n2 = n1 + 2 * (num_elements_y - row) + 1 + row
                n3 = n2 + (num_elements_y - row) + 1 + 2 * row
                n4 = n3 + 1
                n5 = n3 + 2
                n6 = n2 + 1
                n7 = n1 + 2
                n8 = n1 + 1
                self.geometry.add_element([self.geometry.nodes[n1],
                                           self.geometry.nodes[n2],
                                           self.geometry.nodes[n3],
                                           self.geometry.nodes[n4],
                                           self.geometry.nodes[n5],
                                           self.geometry.nodes[n6],
                                           self.geometry.nodes[n7],
                                           self.geometry.nodes[n8]])
