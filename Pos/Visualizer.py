import matplotlib.pyplot as plt
import matplotlib.tri as tri

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
            elif node.is_constrained_x():
                ax.plot(node.x, node.y, 'ro', markersize=10, zorder=5)
                constrained_x_added = True
            elif node.is_constrained_y():
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
            elif node.is_constrained_x():
                ax.plot(node.x + scale_factor * displacements[node.global_index_x], node.y + scale_factor * displacements[node.global_index_y], 'ro', markersize=10, label=node.label, zorder=5)
                constrained_x_added = True
            elif node.is_constrained_y():
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
        # Get plot size in figure coordinates
        _, y = ax.transAxes.inverted().transform((0, 0))

        legend_elements = []
        if constrained_both_added:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='m', label='Constrained (x & y)'))
        if constrained_x_added:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='r', label='Constrained (x)'))
        if constrained_y_added:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='g', label='Constrained (y)'))
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='b', label='Free'))
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, y), title='Legend')

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

    def visualize_displacement(self, displacements, direction: str = 'x', scale_factor: Optional[float] = 1.0):
        """Visualize a color map of the nodal displacement."""

        if direction == 'x':
            title = 'Displacement in x direction'
            displacement_dir = [displacements[node.global_index_x] if node.global_index_x != -1 else 0 for node in self.nodes]
        elif direction == 'y':
            title = 'Displacement in y direction'
            displacement_dir = [displacements[node.global_index_y] if node.global_index_y != -1 else 0 for node in self.nodes]
        else:
            raise ValueError("Invalid direction. Choose from 'x' or 'y'.")

        self.visualize_nodal_field(displacement_dir, 'Displacement', title, displacements, scale_factor)

    def visualize_nodal_stress(self, stress_component: str, displacements: List[float], scale_factor: Optional[float] = 1.0):
        """Visualize a color map of the nodal stress."""

        # Extract the specified stress component
        if stress_component == 'xx':
            stress = [node.stress_avg[0] for node in self.nodes]
            title = 'Stress xx'
        elif stress_component == 'yy':
            stress = [node.stress_avg[1] for node in self.nodes]
            title = 'Stress yy'
        elif stress_component == 'xy':
            stress = [node.stress_avg[2] for node in self.nodes]
            title = 'Stress xy'
        else:
            raise ValueError("Invalid stress component. Choose from 'xx', 'yy', or 'xy'.")

        self.visualize_nodal_field(stress, 'Stress', title, displacements, scale_factor)

    def visualize_nodal_strain(self, strain_component: str, displacements: List[float], scale_factor: Optional[float] = 1.0):
        """Visualize a color map of the nodal strain."""

        # Extract the specified strain component
        if strain_component == 'xx':
            strain = [node.strain_avg[0] for node in self.nodes]
            title = 'Strain xx'
        elif strain_component == 'yy':
            strain = [node.strain_avg[1] for node in self.nodes]
            title = 'Strain yy'
        elif strain_component == 'xy':
            strain = [node.strain_avg[2] for node in self.nodes]
            title = 'Strain xy'
        else:
            raise ValueError("Invalid strain component. Choose from 'xx', 'yy', or 'xy'.")

        self.visualize_nodal_field(strain, 'Strain', title, displacements, scale_factor)

    def visualize_nodal_field(self, field: [], field_name: str, title: str, displacements: List[float] = None, scale_factor: Optional[float] = 1.0):
        """Visualize a color map of a field."""

        # Create new plot
        _, ax = plt.subplots(figsize=(12, 9))

        x = [node.x + scale_factor * displacements[node.global_index_x] for node in self.nodes]
        y = [node.y + scale_factor * displacements[node.global_index_y] for node in self.nodes]

        elem_nodes_map = [[] for _ in self.elements]

        for i, elem in enumerate(self.elements):
            for node in elem.nodes:
                elem_nodes_map[i].append(node.label - 1)

        # convert all elements into triangles
        elements_all_tris = self.shapes_to_tris(elem_nodes_map)

        # create an unstructured triangular grid instance
        triangulation = tri.Triangulation(x, y, elements_all_tris)

        # plot the finite element mesh
        self.plot_fem_mesh(x, y, elem_nodes_map)

        """
        Choose one of the following color maps:
        'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 
        'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 
        'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 
        'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 
        'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 
        'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 
        'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone',
        'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper',
        'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r',
        'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 
        'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r',
        'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 
        'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 
        'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r',
        'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 
        'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'
        """

        # plot the contours
        plt.tricontourf(triangulation, field, cmap='jet', levels=40)

        ax.set_title(title)
        ax.set_aspect('equal', adjustable='box')

        # Plot elements grid
        for element in self.elements:
            for i in range(len(element.nodes)):
                node1 = element.nodes[i]
                node2 = element.nodes[(i + 1) % len(element.nodes)]  # Connect last node with first node
                ax.plot([node1.x + scale_factor * displacements[node1.global_index_x], node2.x + scale_factor * displacements[node2.global_index_x]],
                        [node1.y + scale_factor * displacements[node1.global_index_y], node2.y + scale_factor * displacements[node2.global_index_y]],
                        '-', linewidth=0.1, color='black')

        # Show max and min stress values
        max_field = max(field)
        min_field = min(field)

        # Get plot size in figure coordinates
        x, y = ax.transAxes.inverted().transform((0, 0))

        ax.text(0, y - 0.1, f'Max {field_name}: {max_field:.6f}\nMin {field_name}: {min_field:.6f}', fontsize=10, color='black', transform=ax.transAxes)

        # show
        plt.colorbar()
        plt.show()

    def shapes_to_tris(self, shapes):
        """
        This function converts a list of shapes into a list of triangles
        :param shapes: list of shapes
        :return: list of triangles
        """

        tris = []
        for shape in shapes:
            if len(shape) == 3:
                tris.append(shape)
            elif len(shape) == 4:
                tris.extend(self.quads_to_tris(shape))
            elif len(shape) == 8:
                tris.extend(self.convert_to_6tris(shape))
            else:
                raise ValueError("Invalid shape. Must be a triangle, quad, or 8-node quad.")
        return tris

    @staticmethod
    def convert_to_6tris(quad):
        """
        This is the shape you would get by converting a quad to 6 triangles
                            A---B---C
                            |  /|\  |
                            | / | \ |
                            H\  |  \D
                            | \ |  /|
                            |  \|/  |
                            G---F---E

        :param quads: list of quads

        :return: list of triangles
        """
        tris = []
        # First triangle
        tris.append([quad[0], quad[1], quad[7]])
        # Second triangle
        tris.append([quad[1], quad[2], quad[3]])
        # Third triangle (diagonal-based)
        tris.append([quad[3], quad[4], quad[5]])
        # Fourth triangle (diagonal-based)
        tris.append([quad[5], quad[6], quad[7]])
        # Fifth triangle (diagonal-based)
        tris.append([quad[1], quad[5], quad[7]])
        # Sixth triangle (diagonal-based)
        tris.append([quad[1], quad[5], quad[3]])
        return tris

    # converts quad elements into tri elements. Reference: https://stackoverflow.com/questions/52202014/how-can-i-plot-2d-fem-results-using-matplotlib
    @staticmethod
    def quads_to_tris(quad):
        """
        This is the shape you would get by converting a quad to 2 triangles
                            A-------B
                            |     / |
                            |    /  |
                            |   /   |
                            |  /    |
                            | /     |
                            D-------C

        :param quads: list of quads

        :return: list of triangles
        """
        tris = []
        # First triangle
        tris.append([quad[0], quad[1], quad[2]])
        # Second triangle
        tris.append([quad[2], quad[3], quad[0]])

        return tris

    @staticmethod
    def convert_to_4tris(quads):
        """
        This is the shape you would get by converting a quad to 4 triangles
                            A-------B
                            | \   / |
                            |  \ /  |
                            |   X   |
                            |  / \  |
                            | /   \ |
                            D-------C

        :param quads: list of quads

        :return: list of triangles
        """
        tris = []
        for quad in quads:
            # First triangle
            tris.append([quad[0], quad[1], quad[2]])
            # Second triangle
            tris.append([quad[0], quad[2], quad[3]])
            # Third triangle (diagonal-based)
            tris.append([quad[0], quad[1], quad[3]])
            # Fourth triangle (diagonal-based)
            tris.append([quad[1], quad[2], quad[3]])
        return tris

    # plots a finite element mesh
    def plot_fem_mesh(self, nodes_x, nodes_y, elements):
        for element in elements:
            x = [nodes_x[element[i]] for i in range(len(element))]
            y = [nodes_y[element[i]] for i in range(len(element))]
            plt.fill(x, y, edgecolor='black', fill=False)
