from Engine.Runner import Runner

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runner = Runner()

    # Creating a beam geometry
    runner.construct_beam_geometry()

    # Setting the material
    linear_elastic_material = runner.set_linear_elastic_material(young_modulus=200000., poisson_ratio=0.3, thickness=5.)

    # Boundary conditions
    # engine.set_boundary_conditions(2, False, True)  # Node 3
    runner.set_boundary_conditions(18, True, True)  # Node 19
    runner.set_boundary_conditions(19, True, True)  # Node 20
    runner.set_boundary_conditions(20, True, True)  # Node 21

    # Applying loads
    runner.apply_nodal_load(1, 0, -1000)  # Node 2
    # engine.apply_nodal_load(4, 0, -5000)  # Node 5
    # engine.apply_nodal_load(7, 1000, 7000)  # Node 8

    # Analysis and results
    runner.run_analysis()
    runner.show_results()
