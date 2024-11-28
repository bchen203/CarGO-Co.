import sys
sys.path.append('../CargoCo')
import calculate
import manifest


#array = [[manifest.Container(0, "UNUSED",-1) for col in range(12)] for row in range(8)]

fileName = "SampleManifests/customManifest.txt"
inputManifest = manifest.Manifest(fileName)
array, containerID = inputManifest.copyManifest()
calculator = calculate.Calculate(array, containerID)

print("Initial State of the Manifest:")
print("----------")
for r in range(7, -1, -1):
    for c in range(12):
        print(str(array[r][c].id).rjust(2, " "), end=" ")
    print("")
print("----------")

print("\nTesting is_start_legal function:")
print("TEST 1:")
print("Test is successful if 4 statements of '[ERROR] start position is out of bounds' are printed")
print("----------")
#TEST 1: is_start_legal - testing out of bounds error checking
calculator.is_start_legal(6,12)
calculator.is_start_legal(6,-1)
calculator.is_start_legal(12,6)
calculator.is_start_legal(-1,6)
print("----------")

print()
print("\nTEST 2:")
print("Test is successful if '[ERROR] cannot move container because there is container above starting position' is printed")
print("----------")
#TEST 2: is_start_legal - has container above start position
calculator.is_start_legal(0,0)
print("----------")

print()
print("\nTEST 3:")
print("Test is successful if '[ERROR] cannot move a container with the name \"UNUSED\" or \"NAN\"' is printed")
print("----------")
#TEST 3: is_start_legal - is start position empty
calculator.is_start_legal(1,1)
print("----------")

print()
print("\nTEST 4:")
print("Test is successful if \"Starting position is legal\" is printed followed by \"[ERROR] cannot move a container with the name \"UNUSED\" or \"NAN\" and \"Starting position is not legal\" being printed on the next two lines")
print("----------")
#TEST 4 is_start_legal - is valid start position
if(calculator.is_start_legal(0,1)):
    print("Starting position is legal")
else:
    print("Starting position is not legal")
if(calculator.is_start_legal(1,1)):
    print("Starting position is legal")
else:
    print("Starting position is not legal")
print("----------")

print()
print("\nTesting is_end_legal function:")
print("TEST 5:")
print("Test is successful if 4 statements of '[ERROR] end position is out of bounds' are printed")
print("----------")
#TEST 5: is_end_legal - testing out of bounds error checking
calculator.is_end_legal(6,12)
calculator.is_end_legal(6,-1)
calculator.is_end_legal(12,6)
calculator.is_end_legal(-1,6)
print("----------")

print()
print("\nTEST 6:")
print("Test is successful if '[ERROR] cannot move a container to an occupied location' is printed twice")
print("----------")
#TEST 6: is_end_legal - is end position occupied
calculator.is_end_legal(0,0)
calculator.is_end_legal(0,1)
print("----------")

print()
print("\nTEST 7:")
print("Test is successful if '[ERROR] cannot move container to location where it is floating' is printed ")
print("----------")
#TEST 7 is_end_legal - is end position floating
calculator.is_end_legal(4,4)
print("----------")

print()
print("\nTEST 8:")
print("Test is successful if \"[ERROR] cannot move a container to an occupied location\" is printed followed by \"Ending position is not legal\" and \"Ending position is legal\" being printed on the next two lines")
print("----------")
#TEST 8 is_end_legal - is end position legal
if(calculator.is_end_legal(0,1)):
    print("Ending position is legal")
else:
    print("Ending position is not legal")
if(calculator.is_end_legal(1,1)):
    print("Ending position is legal")
else:
    print("Ending position is not legal")
print("----------")

print()
print("\nTEST 9:")
print("Testing is_legal_ship_move function:")
print("Test is successful if \"Move is legal\" is printed")
print("----------")
#TEST 9 is_legal_ship move - evaluates true when both start and end positions are valid
if(calculator.is_legal_ship_move(0,1,0,5)):
    print("Move is legal")
else:
    print("Move is not legal")
print("----------")

print()
print("\nTEST 10:")
print("Test is successful if \"Move is not legal\" is printed three times. The first and third tests should print an error message saying \"[ERROR] cannot move a container with the name \"UNUSED\" or \"NAN\"\" and the second test should print an error message saying \"[ERROR] cannot move container to location where it is floating\"")
print("----------")
#TEST 10 is_legal_ship move - evaluates false when either start and end positions are invalid
if(calculator.is_legal_ship_move(2,2,5,0)): #when start pos is not legal and end pos is legal
    print("Move is legal")
else:
        print("Move is not legal")

if(calculator.is_legal_ship_move(0,1,5,1)): #when start pos is legal and end pos is not legal
    print("Move is legal")
else:
        print("Move is not legal")

if(calculator.is_legal_ship_move(2,2,5,1)): #when both pos are not legal
    print("Move is legal")
else:
        print("Move is not legal")
print("----------")

print()
print("\nTesting moveContainer function:")
print("TEST 11:")
#TEST 11 moveContainer - moves container when positions are legal
print("Test is successful if \"Container successfully moved\" is printed")
print("----------")
calculator.moveContainer(0,1,2,0)
if(calculator.ship_bay_array[0][1].description == "UNUSED" and calculator.ship_bay_array[2][0].description != "UNUSED"):
        print("Container successfully moved")
else:
        print("Container failed to move")
calculator.moveContainer(2,0,0,1)
print("----------")

print()
print("\nTEST 12:")
print("Test is successful if \"Container failed to move\" is printed with the error message \"[ERROR] cannot move container because there is container above starting position\"")
#TEST 12 moveContainer - don't move container when positions are not both legal
print("----------")
calculator.moveContainer(0,0,2,0)
if(calculator.ship_bay_array[0][0].description == "UNUSED" and calculator.ship_bay_array[2][0].description != "UNUSED"):
        print("Container successfully moved")
else:
        print("Container failed to move")
print("----------")

print()
print("\nTesting loadContainer function:")
print("TEST 13:")
print("Test is successful if \"Container successfully placed on ship\" is printed")
print("----------")
#TEST 13 loadContainer - place container on ship successfully
calculator.loadContainer("CillianCargos",0,3)
if(calculator.ship_bay_array[0][3].description != "UNUSED"):
        print("Container successfully placed on ship")
else:
        print("Container unsuccessful in placing on ship")
print("----------")

print()
#TEST 13.5 loadContainer/generateID - testing unique IDs of loaded containers
print("\nTEST 13.5:")
print("Test is successful if the 4th column contains the numbers: 3,4,5,6,8")
print("----------")
calculator.loadContainer("DillianCargos",1,3)
calculator.loadContainer("EillianCargos",2,3)
calculator.loadContainer("FillianCargos",3,3)
calculator.loadContainer("GillianCargos",4,3)
calculator.offloadContainer(4,3)
calculator.loadContainer("HillianCargos",4,3)
for r in range(7, -1, -1):
    for c in range(12):
        print(str(array[r][c].id).rjust(2, " "), end=" ")
    print("")
print("----------")

print()
print("\nTEST 14:")
print("Test is successful if \"Container unsuccessful in placing on ship\" is printed with the error message \"[ERROR] cannot move a container to an occupied location\"")
print("----------")
#TEST 14 loadContainer - fail to place container on ship - container name valid
calculator.loadContainer("RogerRugs",0,0)
if(calculator.ship_bay_array[0][0].description == "RogerRugs"):
        print("Container successfully placed on ship")
else:
        print("Container unsuccessful in placing on ship")
print("----------")

print()
print("\nTEST 15:")
print("Test is successful if \"[ERROR] cannot load a container with the name \"UNUSED\" or \"NAN\"\" is printed")
print("----------")
#TEST 15 loadContainer - fail to place container on ship - container name invalid
calculator.loadContainer("UNUSED",5,0)
print("----------")

print()
print("\nTesting offloadContainer function:")
print("TEST 16:")
print("Test is successful if \"Container successfully offloaded from ship\" is printed")
print("----------")
#TEST 16 offloadContainer - successfully offload a container from the ship
calculator.offloadContainer(0,1)
if(calculator.ship_bay_array[0][1].description == "UNUSED"):
        print("Container successfully offloaded from ship")
else:
        print("Container unsuccessfully offloaded from ship")
print("----------")


print()
print("\nTEST 17:")
print("Test is successful if \"[ERROR] cannot load a container with the name \"UNUSED\" or \"NAN\"\" is printed")
print("----------")
#TEST 17 offloadContainer - unsuccessfully try to offload a container
calculator.offloadContainer(7,0)
print("----------")

print()
print("\nTesting calculate_time function:")
print("TEST 18:")
print("Test is successful if \"Time calculation is correct\" is printed three times")
print("----------")
#TEST 18 calculate_time - compute manhattan distance
if calculator.calculate_time(8,5,6,4) == 3:
        print("Time calculation is correct")
else:
        print("Time calculation is incorrect")
if calculator.calculate_time(6,4,8,5) == 3:
        print("Time calculation is correct")
else:
        print("Time calculation is incorrect")
if calculator.calculate_time(1,1,1,1) == 0:
        print("Time calculation is correct")
else:
        print("Time calculation is incorrect")
print("----------")

print("\n\nTesting updateManifest function from Manifest class:")
print("TEST 19:")
print("Test is successful if the 4th column contains the numbers: 3,4,5,6,8")
print("----------")
#TEST 19 updateManifest - update the manifest class with this manifest
inputManifest.updateManifest(array)
inputManifest.printManifest()
inputManifest.exportManifest() # NOTE: loaded containers have a weight of -1 since they haven't been given a measured weight from the operator
print("----------")