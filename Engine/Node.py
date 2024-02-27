class Node(object):
    """
    Represents a node in structural analysis.

    Attributes:
        x (float): X-coordinate of the node.

        y (float): Y-coordinate of the node.

        label: Label of the node.

        x_constraint (bool): Indicates if the node is constrained in the x-direction.

        y_constraint (bool): Indicates if the node is constrained in the y-direction.

        x_load (float): Load applied to the node in the x-direction.

        y_load (float): Load applied to the node in the y-direction.

        global_index_x (int): Global index of the node in the x-direction.

        global_index_y (int): Global index of the node in the y-direction.

        stress (list): Stress values from all elements connected to the node.

        strain (list): Strain values from all elements connected to the node.

        stress_avg: Average stress value at the node.

        strain_avg: Average strain value at the node.
    """

    def __init__(self, x: float, y: float):
        """
        Initializes a Node object with given coordinates.

        Args:
            x (float): X-coordinate of the node.

            y (float): Y-coordinate of the node.
        """
        self.label = None
        self.x = x
        self.y = y
        self.x_constraint = False
        self.y_constraint = False

        # Load
        self.x_load = 0.0
        self.y_load = 0.0

        # Global index
        self.global_index_x = -1
        self.global_index_y = -1

        # Stress and strain from all elements
        self.stress = []
        self.strain = []

        # Average stress and strain
        self.stress_avg = None
        self.strain_avg = None

    @property
    def name(self):
        """Returns the name of the node."""
        return f'Node({self.x},{self.y})'

    def __str__(self):
        """Returns a string representation of the node."""
        return self.name

    def __eq__(self, other):
        """Checks if two nodes are equal based on their coordinates."""
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """Returns the hash value of the node based on its coordinates."""
        return hash((self.x, self.y))

    def constrain(self, x: bool, y: bool):
        """
        Sets the constraint status of the node in the x and y directions.

        Args:
            x (bool): True if the node is constrained in the x-direction, False otherwise.

            y (bool): True if the node is constrained in the y-direction, False otherwise.
        """
        self.x_constraint = x
        self.y_constraint = y

    def is_constrained_x(self):
        """Returns True if the node is constrained in the x-direction, False otherwise."""
        return self.x_constraint

    def is_constrained_y(self):
        """Returns True if the node is constrained in the y-direction, False otherwise."""
        return self.y_constraint

    def unconstrain(self):
        """Removes any constraints applied to the node."""
        self.x_constraint = False
        self.y_constraint = False

    def apply_load(self, x: float, y: float):
        """
        Applies loads to the node in the x and y directions.

        Args:
            x (float): Load applied to the node in the x-direction.

            y (float): Load applied to the node in the y-direction.
        """
        self.x_load = x
        self.y_load = y

    def set_global_index_x(self, index: int):
        """
        Sets the global index of the node in the x-direction.

        Args:
            index (int): Global index of the node in the x-direction.
        """
        self.global_index_x = index

    def set_global_index_y(self, index: int):
        """
        Sets the global index of the node in the y-direction.

        Args:
            index (int): Global index of the node in the y-direction.
        """
        self.global_index_y = index
