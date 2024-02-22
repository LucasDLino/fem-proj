import matplotlib.pyplot as plt
from typing import List, Optional

from Engine.Element import Element
from Engine.Node import Node


class Visualizer:
    def __init__(self, nodes: List[Node], elements: List[Element]):
        self.nodes = nodes
        self.elements = elements

    def create_undeformed_geometry(self):
        # create a figure
        fig = plt.figure(figsize=(12, 9))
        constrained_x_added = False
        constrained_y_added = False
        constrained_both_added = False
        for node in self.nodes:
            if node.is_constrained_x() and node.is_constrained_y():
                plt.plot(node.x, node.y, 'mo', markersize=10)
                constrained_both_added = True
            elif node.is_constrained_x() and not constrained_x_added:
                plt.plot(node.x, node.y, 'ro', markersize=10)
                constrained_x_added = True
            elif node.is_constrained_y() and not constrained_y_added:
                plt.plot(node.x, node.y, 'go', markersize=10)
                constrained_y_added = True
            else:
                plt.plot(node.x, node.y, 'bo', markersize=10)

        for element in self.elements:
            for i in range(len(element.nodes)):
                node1 = element.nodes[i]
                node2 = element.nodes[(i + 1) % len(element.nodes)]  # Connect last node with first node
                plt.plot([node1.x, node2.x], [node1.y, node2.y], 'b-', linewidth=1)

        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Geometry Visualization')
        plt.grid(True)
        plt.gca().set_aspect('equal', adjustable='box')

        # Only add legend items that have been used
        self.add_labels(constrained_both_added, constrained_x_added, constrained_y_added)

        return fig

    def create_deformed_geometry(self, displacements: List[float], scale_factor: float, add_nodal_forces: Optional[bool] = False):
        fig = plt.figure(figsize=(12, 9))

        ax = fig.gca()

        constrained_x_added = False
        constrained_y_added = False
        constrained_both_added = False
        for node in self.nodes:
            if node.is_constrained_x() and node.is_constrained_y():
                plt.plot(node.x + scale_factor * displacements[node.global_index_x], node.y + scale_factor * displacements[node.global_index_y], 'mo', markersize=10)
                constrained_both_added = True
            elif node.is_constrained_x() and not constrained_x_added:
                plt.plot(node.x + scale_factor * displacements[node.global_index_x], node.y + scale_factor * displacements[node.global_index_y], 'ro', markersize=10)
                constrained_x_added = True
            elif node.is_constrained_y() and not constrained_y_added:
                plt.plot(node.x + scale_factor * displacements[node.global_index_x], node.y + scale_factor * displacements[node.global_index_y], 'go', markersize=10)
                constrained_y_added = True
            else:
                plt.plot(node.x + scale_factor * displacements[node.global_index_x], node.y + scale_factor * displacements[node.global_index_y], 'bo', markersize=10, )

        for element in self.elements:
            for i in range(len(element.nodes)):
                node1 = element.nodes[i]
                node2 = element.nodes[(i + 1) % len(element.nodes)]  # Connect last node with first node
                plt.plot([node1.x + scale_factor * displacements[node1.global_index_x], node2.x + scale_factor * displacements[node2.global_index_x]],
                         [node1.y + scale_factor * displacements[node1.global_index_y], node2.y + scale_factor * displacements[node2.global_index_y]], 'b-', linewidth=1)

        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Deformed Geometry Visualization')
        ax.grid(True)
        ax.set_aspect('equal', adjustable='box')

        # Only add legend items that have been used
        self.add_labels(constrained_both_added, constrained_x_added, constrained_y_added)

        return fig

    @staticmethod
    def add_labels(constrained_both_added, constrained_x_added, constrained_y_added):
        legend_elements = []
        if constrained_both_added:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='m', label='Constrained (x & y)'))
        if constrained_x_added:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='r', label='Constrained (x)'))
        if constrained_y_added:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='g', label='Constrained (y)'))
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='b', label='Free'))
        plt.legend(handles=legend_elements, loc='upper right')

    def add_nodal_forces_to_figure(self, fig, displacements: List[float]):
        ax = fig.gca()

        # Calculate the minimum element size or any other criterion
        min_element_size = min(element.size() for element in self.elements)  # Example calculation of the minimum element size

        # Define a fraction of the element size to scale down the forces
        force_scaling_factor = min_element_size * 0.05  # Adjust the fraction as needed

        for node in self.nodes:
            force_x = node.x_load
            force_y = node.y_load

            # Scale down the forces if they exceed the specified fraction of the element size
            if abs(force_x) > force_scaling_factor or abs(force_y) > force_scaling_factor:
                scaling_factor_x = force_scaling_factor / abs(force_x) if abs(force_x) != 0 else 1
                scaling_factor_y = force_scaling_factor / abs(force_y) if abs(force_y) != 0 else 1

                # Apply the minimum scaling factor to ensure the force magnitude is less than the element size
                scaling_factor = min(scaling_factor_x, scaling_factor_y)

                # Apply the scaling factor to both force components
                scaled_force_x = force_x * scaling_factor
                scaled_force_y = force_y * scaling_factor

                ax.arrow(node.x + displacements[node.global_index_x],
                         node.y + displacements[node.global_index_y],
                         scaled_force_x,
                         scaled_force_y,
                         color='purple', width=0.3, head_width=1, length_includes_head=True, zorder=10)
        return fig

    def visualize_undeformed_geometry(self):
        self.create_undeformed_geometry()
        plt.show()

    def visualize_deformed_geometry(self, displacements: List[float], scale_factor: float, add_nodal_forces: Optional[bool] = False):
        fig = self.create_deformed_geometry(displacements, scale_factor, add_nodal_forces)
        if add_nodal_forces:
            self.add_nodal_forces_to_figure(fig, displacements)
        plt.show()
