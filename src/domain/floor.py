class Floor:
    def __init__(self, db_id=None, name=None):
        self.__db_id = db_id
        self.__name = name
        self.__grid_size = (10, 10)

        self.__elements = {}
        self.__grid = {}
        self.__connections = {}

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def elements(self):
        return self.__elements

    @property
    def grid(self):
        return self.__grid

    @property
    def connections(self):
        return self.__connections




    def load_element(self, element):
        self.__elements[element.element_id] = element
        self.__grid[element.position] = element
        self.add_connections(element)


    # def move_element(self, element, new_position):
    #     if element.element_id not in self.__elements or new_position in self.__grid:
    #         raise Exception('Element doesn\'t exist or space occupied')
    #
    #     self.__grid.pop(element.position)
    #     self.__elements[element.element_id].position = new_position
    #     self.__grid[element.position] = element
    #
    #     self.handle_connections(element)




    def add_connections(self, element):
        if element.connections:
            return

        neighbors = self.get_neighbors(element)
        for neighbor in neighbors.values():
            if self.can_connect_to(element, neighbor) and self.can_connect_to(neighbor, element):
                self.connect(element.element_id, neighbor.element_id)
                if element.element_type == "room":
                    break

    def remove_connections(self, element):
        pass



    def connect(self, id1, id2):
        el1 = self.__elements[id1]
        el2 = self.__elements[id2]

        if id1 not in self.__connections:
            self.__connections[id1] = set()
        if id2 not in self.__connections:
            self.__connections[id2] = set()

        self.__connections[id1].add(id2)
        self.__connections[id2].add(id1)

        if not el1.connections:
            el1.connections = set()
        if not el2.connections:
            el2.connections = set()

        el1.connections.add(id2)
        el2.connections.add(id1)


    def disconnect(self, id1, id2):
        pass



    def get_neighbors(self, element):
        x, y = element.position
        neighbor_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        neighbors = {}
        for pos in neighbor_positions:
            if pos in self.__grid:
                neighbors[pos] = self.__grid[pos]
        return neighbors

    def is_neighbor(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2) == 1

    def can_connect_to(self, element1, element2):
        if element1.element_type == 'room':
            return (element2.element_type in {'hallway', 'staircase'} and
                    self.is_neighbor(element1.position, element2.position) and
                    (not element1.connections or len(element1.connections) < 1))
        elif element1.element_type == 'hallway' and self.is_neighbor(element2.position, element1.position):
            return not element1.connections or len(element1.connections) < 4
        elif element1.element_type == 'staircase' and (
                self.is_neighbor(element2.position, element1.position) or
                element1.floor_name != element2.floor_name):
            return not element1.connections or len(element1.connections) < 6
        return False