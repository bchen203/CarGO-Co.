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
        self.filename = filename
        file = open(self.filename, "r")
        lines = file.readlines()

        for line in lines:
            temp = line.split(",")

            x = int(temp[0][1:])
            y = int(temp[1][:2])
            weight = re.search("[0-9]{5}", temp[2])
            description = temp[3][1:]

            self.grid[y - 1][x - 1] = Container(int(weight.group()), description)

    def exportManifest(self):
        file = open("Output_Manifest.txt", "w")
        for i in range(8):
            for j in range(12):
                temp = self.grid[j][i]
                padded_x = str(i + 1).rjust(2, "0")
                padded_y = str(j + 1).rjust(2, "0")
                padded_weight = str(temp.weight).rjust(5, "0")

                output = f"[{padded_x}, {padded_y}], {{{padded_weight}}}, {temp.description}"

                file.write(output)
        file.close()
