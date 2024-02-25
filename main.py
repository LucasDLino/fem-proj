from Engine.Runner import Runner
from Examples import examples_reader


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runner = Runner()

    nodes, elements, nodes_restrictions, nodes_forces, elements_material = examples_reader.read_json_file('Examples/9_70_bana.json')


    # Creating a beam geometry
    runner.construct_beam_geometry(nodes, elements)

    # Setting the material
    linear_elastic_material = runner.set_linear_elastic_material(young_modulus=elements_material['E'], poisson_ratio=elements_material['poisson'], thickness=elements_material['thickness'])

    # Boundary conditions
    for node, (x, y) in nodes_restrictions.items():
        runner.set_boundary_conditions(int(node), x, y)

    for node, (x, y) in nodes_forces.items():
        runner.apply_nodal_load(int(node), x, y)


    # Applying loads
    # runner.apply_nodal_load(78, 0, -30000)  # Node 2
    # engine.apply_nodal_load(4, 0, -5000)  # Node 5
    # engine.apply_nodal_load(7, 1000, 7000)  # Node 8

    # Analysis and results
    runner.run_analysis()
    runner.show_results()
