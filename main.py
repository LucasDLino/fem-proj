from Engine.Runner import Runner

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runner = Runner()

    # Creating a beam geometry
    runner.construct_beam_geometry()

    # Setting the material
    linear_elastic_material = runner.set_linear_elastic_material(young_modulus=40000., poisson_ratio=0.17, thickness=100)

    # Boundary conditions
    # engine.set_boundary_conditions(2, False, True)  # Node 3
    runner.set_boundary_conditions(14, False, True)
    runner.set_boundary_conditions(112, True, False)
    runner.set_boundary_conditions(113, True, False)
    runner.set_boundary_conditions(114, True, False)
    runner.set_boundary_conditions(115, True, False)
    runner.set_boundary_conditions(116, True, False)
    runner.set_boundary_conditions(117, True, False)
    runner.set_boundary_conditions(118, True, False)
    runner.set_boundary_conditions(119, True, False)
    runner.set_boundary_conditions(120, True, False)


    # Applying loads
    runner.apply_nodal_load(78, 0, -30000)  # Node 2
    # engine.apply_nodal_load(4, 0, -5000)  # Node 5
    # engine.apply_nodal_load(7, 1000, 7000)  # Node 8

    # Analysis and results
    runner.run_analysis()
    runner.show_results()
