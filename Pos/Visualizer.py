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

        ax = fig.gca()

        label_offset = 0.4

        constrained_x_added = False
        constrained_y_added = False
        constrained_both_added = False

        for node in self.nodes:
            if node.is_constrained_x() and node.is_constrained_y():
                ax.plot(node.x, node.y, 'mo', markersize=10, zorder=5)
                constrained_both_added = True
            elif node.is_constrained_x() and not constrained_x_added:
                ax.plot(node.x, node.y, 'ro', markersize=10, zorder=5)
                constrained_x_added = True
            elif node.is_constrained_y() and not constrained_y_added:
                ax.plot(node.x, node.y, 'go', markersize=10, zorder=5)
                constrained_y_added = True
            else:
                ax.plot(node.x, node.y, 'bo', markersize=10, zorder=5)

            ax.text(node.x + label_offset,
                    node.y + label_offset,
                    f'{node.label}',  # Change 'Node' to your desired label
                    fontsize=10,  # Adjust font size as needed
                    color='black')  # Adjust color as needed

        for element in self.elements:
            for i in range(len(element.nodes)):
                node1 = element.nodes[i]
                node2 = element.nodes[(i + 1) % len(element.nodes)]  # Connect last node with first node
                plt.plot([node1.x, node2.x], [node1.y, node2.y], 'b-', linewidth=1)

        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Geometry Visualization')
        ax.grid(True)
        ax.set_aspect('equal', adjustable='box')

        # Only add legend items that have been used
        self.add_labels(ax, constrained_both_added, constrained_x_added, constrained_y_added)

        return fig

    def create_deformed_geometry(self, displacements: List[float], scale_factor: Optional[float] = 1.0):
        fig = plt.figure(figsize=(12, 9))

        ax = fig.gca()

        label_offset = 0.6

        constrained_x_added = False
        constrained_y_added = False
        constrained_both_added = False

        for node in self.nodes:
            if node.is_constrained_x() and node.is_constrained_y():
                ax.plot(node.x + scale_factor * displacements[node.global_index_x], node.y + scale_factor * displacements[node.global_index_y], 'mo', markersize=10, label=node.label, zorder=5)
                constrained_both_added = True
            elif node.is_constrained_x() and not constrained_x_added:
                ax.plot(node.x + scale_factor * displacements[node.global_index_x], node.y + scale_factor * displacements[node.global_index_y], 'ro', markersize=10, label=node.label, zorder=5)
                constrained_x_added = True
            elif node.is_constrained_y() and not constrained_y_added:
                ax.plot(node.x + scale_factor * displacements[node.global_index_x], node.y + scale_factor * displacements[node.global_index_y], 'go', markersize=10, label=node.label, zorder=5)
                constrained_y_added = True
            else:
                ax.plot(node.x + scale_factor * displacements[node.global_index_x], node.y + scale_factor * displacements[node.global_index_y], 'bo', markersize=10, label=node.label, zorder=5)

            ax.text(node.x + label_offset + scale_factor * displacements[node.global_index_x],
                    node.y + label_offset + scale_factor * displacements[node.global_index_y],
                    f'{node.label}',  # Change 'Node' to your desired label
                    fontsize=10,  # Adjust font size as needed
                    color='black')  # Adjust color as needed

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
        self.add_labels(ax, constrained_both_added, constrained_x_added, constrained_y_added)

        return fig

    @staticmethod
    def add_labels(ax, constrained_both_added, constrained_x_added, constrained_y_added):
        legend_elements = []
        if constrained_both_added:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='m', label='Constrained (x & y)'))
        if constrained_x_added:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='r', label='Constrained (x)'))
        if constrained_y_added:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='g', label='Constrained (y)'))
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='b', label='Free'))
        ax.legend(handles=legend_elements, loc='upper right')

    def add_nodal_forces_to_figure(self, fig, displacements: List[float], scale_factor: Optional[float] = 1.0):
        ax = fig.gca()

        # Calculate the minimum element size or any other criterion
        min_element_size = min(element.max_size() for element in self.elements)  # Example calculation of the minimum element size

        # Define a fraction of the element size to scale down the forces
        force_scaling_factor = min_element_size * 0.5  # Adjust the fraction as needed

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

                ax.arrow(node.x + scale_factor * displacements[node.global_index_x] - scaled_force_x,
                         node.y + scale_factor * displacements[node.global_index_y] - scaled_force_y,
                         scaled_force_x,
                         scaled_force_y,
                         color='purple', width=0.3, head_width=1, length_includes_head=True, zorder=10)
        return fig

    def create_displacement_table(self, displacements):
        # Create new plot
        fig = plt.figure(figsize=(12, 9))

        ax = fig.gca()

        # Created margins to fit the table
        plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

        # # Define the table data and headers
        headers = ['Node', 'X Displacement', 'Y Displacement']
        table_data = [[f'Node {node.label}', f'{displacements[node.global_index_x]:.6f}', f'{displacements[node.global_index_y]:.6f}'] for node in self.nodes]

        # Create the table and add it to the figure
        table = ax.table(cellText=table_data, colLabels=headers, loc='center', cellLoc='center', colLoc='center')

        # Adjust table properties
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.5, 1.5)  # Adjust scale as needed

        # Hide axes to make the table more visible
        ax.axis('off')

        return fig

    def visualize_undeformed_geometry(self):
        self.create_undeformed_geometry()
        plt.show()

    def visualize_deformed_geometry(self, displacements: List[float], scale_factor: float, add_nodal_forces: Optional[bool] = False):
        fig = self.create_deformed_geometry(displacements, scale_factor)
        if add_nodal_forces:
            self.add_nodal_forces_to_figure(fig, displacements, scale_factor)
        plt.show()

    def visualize_disp_table(self, displacements):
        self.create_displacement_table(displacements)
        plt.show()
