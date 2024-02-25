from Engine.Runner import Runner
from Pre.BeamMeshGenerator import BeamMeshGenerator

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runner = Runner()

    BeamMeshGenerator(runner.geometry).generate_bilinear_mesh(width=60., height=20., num_x_nodes=31, num_y_nodes=11, x_origin=0., y_origin=-10.)

    # Setting the material
    linear_elastic_material = runner.set_linear_elastic_material(young_modulus=200000., poisson_ratio=0.3, thickness=5.)

    # Boundary conditions - constrain all nodes in which x = 60.
    for node in runner.geometry.nodes:
        if node.x == 60.:
            runner.set_boundary_conditions(node.label - 1, True, True)

    # Applying loads - apply a load of 1000 N in the y direction for node with x = 0 and y = 0.
    for node in runner.geometry.nodes:
        if node.x == 0. and node.y == 0.:
            runner.apply_nodal_load(node.label - 1, 0, -1000)

    # Analysis and results
    runner.run_analysis()
    runner.show_results()
