import json


def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        element_type = data.get('element_type', 'quad4')
        geometry = data.get('geometry', {})
        nodes_restrictions = data.get('nodes_restrictions', {})
        nodes_forces = data.get('nodes_forces', {})
        elements_material = data.get('elements_material', {})
        results_dir = data.get('results_dir', 'figs')

        return element_type, geometry, nodes_restrictions, nodes_forces, elements_material, results_dir
