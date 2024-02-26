from Engine.Runner import Runner
from Pre.BeamMeshGenerator import BeamMeshGenerator
from Examples import examples_reader

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runner = Runner()

    # element_type, geometry, nodes_restrictions, nodes_forces, elements_material = examples_reader.read_json_file('Examples/9_49_bana.json')
    element_type, geometry, nodes_restrictions, nodes_forces, elements_material = examples_reader.read_json_file('Examples/something_bana.json')

    if element_type == 'quad4':
        BeamMeshGenerator(runner.geometry).generate_bilinear_mesh(width=geometry['width'], height=geometry['height'], num_elements_x=geometry['num_elements']['x'], num_elements_y=geometry['num_elements']['y'], x_origin=geometry['origin']['x'], y_origin=geometry['origin']['y'])
    elif element_type == 'quad8':
        BeamMeshGenerator(runner.geometry).generate_biquadratic_mesh(width=geometry['width'], height=geometry['height'], num_elements_x=geometry['num_elements']['x'], num_elements_y=geometry['num_elements']['y'], x_origin=geometry['origin']['x'], y_origin=geometry['origin']['y'])
    else:
        raise ValueError('Element type not supported')

    # Setting the material
    linear_elastic_material = runner.set_linear_elastic_material(young_modulus=elements_material['E'], poisson_ratio=elements_material['poisson'], thickness=elements_material['thickness'])

    for node in runner.geometry.nodes:
        for restriction_data in nodes_restrictions:
            pos_x = restriction_data['position']['x']
            pos_y = restriction_data['position']['y']
            if (pos_x is None or pos_x == node.x) and (pos_y is None or pos_y == node.y):
                runner.set_boundary_conditions(node.label - 1, restriction_data['restrictions']['x'], restriction_data['restrictions']['y'])

        for force_data in nodes_forces:
            pos_x = force_data['position']['x']
            pos_y = force_data['position']['y']
            if (pos_x == node.x) and (pos_y == node.y):
                runner.apply_nodal_load(node.label - 1, force_data['forces']['x'], force_data['forces']['y'])

    # Analysis and results
    runner.run_analysis()  # no flag passed, so that mean full integration in both stiffness and stress-strain computation
    runner.show_results(scale_factor=200)
