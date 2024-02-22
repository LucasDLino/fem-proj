class Node(object):  # Although python 3, it is good practice to inherit from object
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.x_constraint = False
        self.y_constraint = False
        self.x_load = 0.0
        self.y_load = 0.0

    @property
    def name(self):
        return f'Node({self.x},{self.y})'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def constrain(self, x: bool, y: bool):
        self.x_constraint = x
        self.y_constraint = y

    def is_constrained(self):
        return self.x_constraint or self.y_constraint

    def is_constrained_x(self):
        return self.x_constraint

    def is_constrained_y(self):
        return self.y_constraint

    def unconstrain(self):
        self.x_constraint = False
        self.y_constraint = False

    def apply_load(self, x: float, y: float):
        self.x_load = x
        self.y_load = y
