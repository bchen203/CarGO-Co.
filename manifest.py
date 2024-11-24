import re


class Container:
    def __init__(self, container_weight, container_description, container_id):
        self.weight = container_weight
        # Note: reserved container names are UNUSED, NAN (will need to check if the operator inputs these names later on)
        self.description = container_description
        # Added id variable to uniquely identify containers (will be used in solution calculations)
        self.id = container_id

    def print(self):
        print(f"container weight: {self.weight}")
        print(f"container description: {self.description}")

    def changeWeight(self, weight):
        # TODO: [LOG] add log here for adding weight to container (this function call will only occur when the operator adds the weight to a container being loaded)
        self.weight = weight


class Manifest:
    # the 2D grid representation of the ship's containers
    # ship dimensions: 12x8
    grid = [[Container(0, "UNUSED", -1) for i in range(8)] for j in range(12)]
    containerID = -1

    # initialize the manifest object by reading in a given manifest file
    def __init__(self, filename):
        # TODO: [LOG] Operator input [manifestfilename]. It has [stats]
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
            # POTENTIAL PROBLEM: by using regex for description, we exclude the newline at the end of each line. This results in the exported manifest also not including the newline, so we have to manually re-add it back, except for on the last line. This assumption of removing the newline on the last line of the file could lead to a mismatched manifest if the original manifest included a newline on the last line.
            description = (re.search("[A-Za-z0-9]+", temp[3])).group()
            if description != "UNUSED" and description != "NAN":
                id = self.generateID()
            else:
                id = -1

            # 3. create a container object using the variables from step 2 and add it to the 2D grid at location [y-1][x-1] (zero indexing adjustment)
            self.grid[y - 1][x - 1] = Container(int(weight.group()), description, id)

    # export the outbound manifest
    def exportManifest(self):
        # TODO: [LOG] exported the manifest with the name [outboundmanifestfilename]
        # creates a new output manifest
        output_file = self.filename[:-4] + "OUTBOUND.txt" # append "OUTBOUND" to end of manifest name
        file = open(output_file, "w")
        for i in range(8):
            for j in range(12):
                temp = self.grid[j][i]
                # ensure that all coordinate locations have a leading zero (each coordinate is 2 digits)
                padded_x = str(i + 1).rjust(2, "0")
                padded_y = str(j + 1).rjust(2, "0")
                # ensure that all weights have leading zeros (each weight is 5 digits)
                padded_weight = str(temp.weight).rjust(5, "0")

                # combine all the data into a singular manifest line
                output = f"[{padded_x},{padded_y}], {{{padded_weight}}}, {temp.description}"

                # write this line to the manifest file
                # check if we are writing the last line of the exported manifest. If so, do not include the newline
                if i == 7 and j == 11:
                    file.write(f"{output}")
                else:
                    file.write(f"{output}\n")
        file.close()

    # return a copy of the manifest
    def copyManifest(self):
        return self.grid
    
    # print the id's of the manifest (for terminal use only)
    def printManifest(self):
        for i in range(7, -1, -1):
            for j in range(12):
                print(self.grid[j][i].id, end=" ")
            print("")

    # returns the next ID needed to uniquely identify a container and will update the manifest class's ID global containerID variable
    def generateID(self):
        self.containerID += 1
        return self.containerID


#commented out and implementation moved to calculate.py
"""
    # move containers that already exist on the ship
    # [y1,x1]: starting location of container (to be replaced with "UNUSED")
    # [y2,x2]: ending location of container (to be replaced with the moved container)
    # ERROR CHECKING: a container can only be moved if the ending location is in the 2D grid range, is "UNUSED", and the container being moved is NOT "UNUSED" nor "NAN"
    def moveContainer(self, y1, x1, y2, x2):
        containerMoving = self.grid[y1,x1]
        if containerMoving.description != "UNUSED" and containerMoving.description != "NAN":
            if self.grid[y2,x2].description == "UNUSED":
                if y2 > 0 and self.grid[y2,x2].description != "UNUSED": #DAVID: checks to see if container would be floating
                    # TODO: [LOG] container [name] was moved from [startLocation] to [endLocation]
                    self.grid[y1,x1] = Container(0, "UNUSED")
                    self.grid[y2,x2] = containerMoving
                else:
                    print("[ERROR] cannot move container to location where it is floating\n")
            else:
                print("[ERROR] cannot move a container to an occupised location\n")
        else:
            print("[ERROR] cannot move a container with the name \"UNUSED\" or \"NAN\"\n")

    # load containers onto the ship
    # containerDescription: the description of a container provided by the operator
    # [y,x]: ending location of container <-- NOTE: in the final implementation, this parameter will be generated by the solution, not the operator
    # ERROR CHECKING: a container can only be loaded if the ending location is in the 2D grid range, is "UNUSED", and the container being moved is NOT "UNUSED" nor "NAN"
    def loadContainer(self, containerDescription, y, x):
        if containerDescription != "UNUSED" and containerDescription != "NAN":
            if self.grid[y,x].description == "UNUSED":
                if y > 0 and self.grid[y,x].description != "UNUSED": #DAVID: checks to see if container would be floating
                    # TODO: [LOG] container [name] was loaded onto the ship. It is located at [y,x]
                    # NOTE: a weight of -1 is given as a placeholder weight since the weight of the container will not be determined until the operator picks up the container during the instruction phase of the program
                    self.grid[y,x] = Container(-1, containerDescription)
                else:
                        print("[ERROR] cannot move container to location where it is floating\n")
            else:
                print("[ERROR] cannot move a container to an occupised location\n")
        else:
            print("[ERROR] cannot load a container with the name \"UNUSED\" or \"NAN\"\n")

    # offload containers onto the ship
    # [y,x]: location of the container to be offloaded <-- NOTE: in the final implementation, this parameter will be generated by the solution, not the operator
    # ERROR CHECKING: a container can only be offloaded if the given location is in the 2D grid range and the container being offloaded is NOT "UNUSED" nor "NAN"
    def offloadContainer(self, y, x):
        if self.grid[y,x].description != "UNUSED" and self.grid[y,x].description != "NAN":
                # TODO: [LOG] container [name] was offloaded from the ship.
                self.grid[y,x] = Container(0, "UNUSED")
        else:
            print("[ERROR] cannot offload a container with the name \"UNUSED\" or \"NAN\"\n")
"""
