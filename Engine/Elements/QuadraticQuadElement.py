from typing import List, Optional

from Engine.Element import Element
from Engine.Material import Material
from Engine.Node import Node


class QuadraticQuadElement(Element):
    def __init__(self, nodes: List[Node] = None, material: Material = Optional[Material]):
        super().__init__(nodes, material)

    @property
    def name(self):
        return 'Quadratic Quadrilateral Element'

    @property
    def max_nodes(self):
        return 8
