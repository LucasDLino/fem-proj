from Engine.Runner import Runner

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    engine = Runner()

    # Creating a beam geometry
    engine.construct_beam_geometry()

    # Setting the material
    linear_elastic_material = engine.set_linear_elastic_material(young_modulus=200000., poisson_ratio=0.3, thickness=5.)

    # Boundary conditions
    # engine.set_boundary_conditions(13, False, True)  # Node 1
    engine.set_boundary_conditions(18, True, True)  # Node 19
    engine.set_boundary_conditions(19, True, True)  # Node 20
    engine.set_boundary_conditions(20, True, True)  # Node 21

    # Applying loads
    engine.apply_nodal_load(1, 0, -1000)  # Node 1
    # engine.apply_nodal_load(4, 0, -5000)  # Node 5
    # engine.apply_nodal_load(7, 1000, 7000)  # Node 8

    # Analysis and results
    engine.run_analysis()
    engine.show_results()
