class Floor:
    def __init__(self, name):
        self.__name = name
        self.__elements = {}
        self.__connections = {}
        self.__grid_size = (10, 10)
        self.__grid = {}


    @property
    def grid(self):
        return self.__grid

    def add_element(self, element):
        self.__elements[element.element_id] = element
        self.__grid[element.position] = element
        self.handle_connections(element)

    def edit_room(self):
        pass

    def move_element(self, element, new_position):
        pass

    def remove_element(self, element):
        pass




    def connect(self, id1, id2):
        if id1 in self.__elements and id2 in self.__elements:
            el1 = self.__elements[id1]
            el2 = self.__elements[id2]
            if el1.can_connect_to(el2) and el2.can_connect_to(el1):
                self.__connections[id1].add(id2)
                self.__connections[id2].add(id1)
                el1.connections.add(id2)
                el2.connections.add(id1)
            else:
                raise Exception("Connection not allowed")

    def handle_connections(self, element):
        if element.connections:
            return

        neighbors = self.get_neighbors(element)
        for neighbor in neighbors.values():
            if element.can_connect_to(neighbor) and neighbor.can_connect_to(element):
                self.connect(element.id, neighbor.id)
                if element.element_type == "room":
                    break

    def get_neighbors(self, element):
        x, y = element.position
        neighbor_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        neighbors = {}
        for pos in neighbor_positions:
            if pos in self.__grid:
                neighbors[pos] = self.__grid[pos]
        return neighbors