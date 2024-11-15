import re


class Container:
    def __init__(self, container_weight, container_description):
        self.weight = container_weight
        # Note: reserved container names are UNUSED, NAN (will need to check if the operator inputs these names later on)
        self.description = container_description

    def print(self):
        print(f"container weight: {self.weight}")
        print(f"conainer description: {self.description}")


class Manifest:
    # the 2D grid representation of the ship's containers
    # ship dimensions: 12x8
    grid = [[Container(0, "UNUSED") for i in range(8)] for j in range(12)]

    # initialize the manifest object by reading in a given manifest file
    def __init__(self, filename):
        self.filename = filename
        file = open(self.filename, "r")
        lines = file.readlines()

        # Sample manifest line: [01, 03], {00100}, Dog
        #                       [yy, xx], {weight}, name
        for line in lines:
            # 1. split the line by commas
            #    temp will store an array of strings split by the commas from line
            #    Ex. temp = {"[01", " 03]", " {00100}", " Dog"}
            temp = line.split(",")

            # 2. get substrings of temp items and store into their respective variables
            x = int(temp[0][1:])
            y = int(temp[1][:2])
            weight = re.search("[0-9]{5}", temp[2])
            description = temp[3][1:]

            # 3. create a container object using the variables from step 2 and add it to the 2D grid at location [y-1][x-1] (zero indexing adjustment)
            self.grid[y - 1][x - 1] = Container(int(weight.group()), description)

    # export the outbound manifest
    def exportManifest(self):
        # creates a new output manifest
        file = open("Output_Manifest.txt", "w")
        for i in range(8):
            for j in range(12):
                temp = self.grid[j][i]
                # ensure that all coordinate locations have a leading zero (each coordinate is 2 digits)
                padded_x = str(i + 1).rjust(2, "0")
                padded_y = str(j + 1).rjust(2, "0")
                # ensure that all weights have leading zeros (each weight is 5 digits)
                padded_weight = str(temp.weight).rjust(5, "0")

                # combine all the data into a singular manifest line
                output = f"[{padded_x}, {padded_y}], {{{padded_weight}}}, {temp.description}"

                # write this line to the manifest file
                file.write(output)
        file.close()
