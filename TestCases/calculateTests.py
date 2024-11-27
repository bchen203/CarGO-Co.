import sys
sys.path.append('../CargoCo')
import calculate
#import manifest


array = [[calculate.Container(0, "UNUSED",-1) for col in range(12)] for row in range(8)]

"""
for i in array:
        print("[")
        for j in i:
            print(j.description)
        print("]")
"""

calculator = calculate.Calculate(array)
array[0][0] = calculate.Container(1,"CoolCatCars",0)
array[0][1] = calculate.Container(2,"DogDerbies",1)
array[1][0] = calculate.Container(3,"ThirdContainer",2)
print("Testing is_start_legal function:")

for r in range(7, -1, -1):
    for c in range(12):
        print(str(array[r][c].id).rjust(2, " "), end=" ")
    print("")


print("TEST 1:")

#TEST 1: is_start_legal - testing out of bounds error checking
calculator.is_start_legal(6,12)
calculator.is_start_legal(6,-1)
calculator.is_start_legal(12,6)
calculator.is_start_legal(-1,6)
print()

print("TEST 2:")
#TEST 2: is_start_legal - has container above start position
calculator.is_start_legal(0,0)
print()
print("TEST 3:")
#TEST 3: is_start_legal - is start position empty
calculator.is_start_legal(1,1)
print()
print("TEST 4:")
#TEST 4 is_start_legal - is valid start position
if(calculator.is_start_legal(0,1)):
    print("Starting position is legal")
else:
    print("Start position is not legal")
if(calculator.is_start_legal(1,1)):
    print("Starting position is legal")
else:
    print("Start position is not legal")

print()
print("Testing is_end_legal function:")
print("TEST 5:")
#TEST 5: is_end_legal - testing out of bounds error checking
calculator.is_end_legal(6,12)
calculator.is_end_legal(6,-1)
calculator.is_end_legal(12,6)
calculator.is_end_legal(-1,6)
print()
print("TEST 6:")
#TEST 6: is_end_legal - is end position occupied
calculator.is_end_legal(0,0)
calculator.is_end_legal(0,1)
print()
print("TEST 7:")
#TEST 7 is_end_legal - is end position floating
calculator.is_end_legal(4,4)
print()
print("TEST 8:")
#TEST 8 is_end_legal - is end position legal
if(calculator.is_end_legal(0,1)):
    print("Ending position is legal")
else:
    print("Ending position is not legal")
if(calculator.is_end_legal(1,1)):
    print("Ending position is legal")
else:
    print("Ending position is not legal")

print()
print("TEST 9:")
print("Testing is_legal_ship_move function:")
#TEST 9 is_legal_ship move - evaluates true when both start and end positions are valid
if(calculator.is_legal_ship_move(0,1,0,5)):
    print("Move is legal")
else:
        print("Move is not legal")

print()
print("TEST 10:")
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

print()
print("Testing moveContainer function:")
print("TEST 11:")
#TEST 11 moveContainer - moves container when positions are legal
#calculator.is_end_legal(0,2)

calculator.moveContainer(0,1,2,0)
if(calculator.ship_bay_array[0][1].description == "UNUSED" and calculator.ship_bay_array[2][0].description != "UNUSED"):
        print("Container successfully moved")
else:
        print("Container failed to move")
calculator.moveContainer(2,0,0,1)

print()
print("TEST 12:")
#TEST 12 moveContainer - don't move container when positions are not both legal
calculator.moveContainer(0,0,2,0)
if(calculator.ship_bay_array[0][0].description == "UNUSED" and calculator.ship_bay_array[2][0].description != "UNUSED"):
        print("Container successfully moved")
else:
        print("Container failed to move")

print()
print("Testing loadContainer function:")
print("TEST 13:")
#TEST 13 loadContainer - place container on ship successfully
calculator.loadContainer("CillianCargos",0,3)
if(calculator.ship_bay_array[0][3].description != "UNUSED"):
        print("Container successfully placed on ship")
else:
        print("Container unsuccessful in placing on ship")

for r in range(7, -1, -1):
    for c in range(12):
        print(str(array[r][c].id).rjust(2, " "), end=" ")
    print("")

print()
print("TEST 14:")
#TEST 14 loadContainer - fail to place container on ship - container name valid
calculator.loadContainer("RogerRugs",0,0)
if(calculator.ship_bay_array[0][0].description == "RogerRugs"):
        print("Container successfully placed on ship")
else:
        print("Container unsuccessful in placing on ship")

print()
print("TEST 15:")
#TEST 15 loadContainer - fail to place container on ship - container name invalid
calculator.loadContainer("UNUSED",5,0)

print()
print("Testing offloadContainer function:")
print("TEST 16:")
#TEST 16 offloadContainer - successfully offload a container from the ship
calculator.offloadContainer(0,1)
if(calculator.ship_bay_array[0][1].description == "UNUSED"):
        print("Container successfully offloaded from ship")
else:
        print("Container unsuccessfully offloaded from ship")

print()
print("TEST 17:")
#TEST 17 offloadContainer - unsuccessfully try to offload a container
calculator.offloadContainer(7,0)

print()
print("Testing calculate_time function:")
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