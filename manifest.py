import re

class Container:
    def __init__(self, container_weight, container_description):
        self.weight = container_weight
        self.description = container_description

    def print(self):
        print(f"container weight: {self.weight}")
        print(f"conainer description: {self.description}")

class Manifest:

    grid = [[Container(0, "UNUSED") for i in range(8)] for j in range(12)]

    def __init__(self, filename):
        file = open(filename, "r")
        lines = file.readlines()

        for line in lines:
            temp = line.split(",")

            x = int(temp[0][1:])
            y = int(temp[1][:2])
            weight = re.search("[0-9]{5}", temp[2])
            description = temp[3]

            self.grid[y - 1][x - 1] = Container(int(weight.group()), description)



