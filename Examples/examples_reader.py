import json

def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

        node_coords = data.get('node_coords', {})
        elements = data.get('elements', [])
        nodes_restrictions = data.get('nodes_restrictions', {})
        nodes_forces = data.get('nodes_forces', {})
        elements_material = data.get('elements_material', {})

        return node_coords, elements, nodes_restrictions, nodes_forces, elements_material