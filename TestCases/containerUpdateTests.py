import sys
sys.path.append('../CargoCo')
import manifest
import calculate





#Test Case 1 - New initialization function
print("Test Case 1 - Testing new initialization")
testContainer = manifest.Container(15, "Something", 0, 1, 2)
testContainer.print()
print(" ")

#Test Case 2 - Comparing Manifest location with container location:
print("Test Case 2 - Comparing if manifest matches container location -> It should")
mani = manifest.Manifest("SampleManifests/customManifest.txt")
mani.printManifest()

manifest_array = mani.copyManifest()[0]
coordinate_1 = [0,1]
coordinate_2 = [1,0]
print(f"Testing Coordinate 1: {coordinate_1}")
print("Container: ")
manifest_array[coordinate_1[0]][coordinate_1[1]].print()

print(f"Testing Coordinate 2: {coordinate_2}")
print("Container: ")
manifest_array[coordinate_2[0]][coordinate_2[1]].print()

print(f"Manifest array: ")
mani.printManifest()

print("Container 2 should be Dog, container 1 should be Cat")


#Test Case 3 - Instantiating and printing Instructions:
print("Testing Case 3 -  Instantiating and printing Instructions")
print("Created instruction with id 45, Start Location (0,1), and End Location (4,6)")
new_instruction = calculate.Instruction(45, (0,1), (4, 6), "TestInstruction")
new_instruction.print()

#Test Case 4 - Testing Calculate.py
print("Testing Case 4 - Calculate.py")
calculator = calculate.Calculate(mani.copyManifest()[0], mani.copyManifest()[1])
#current Manifest
print("Current Array: ")
mani.printManifest()
calculator.loadContainer("Bird Toys", 1,1)
print("Loading 'Bird Toys' to 1,1 ")
mani.updateManifest(calculator.ship_bay_array)
mani.printManifest()
containerInfo = calculator.ship_bay_array[1][1]
print(f"Container Info:")
containerInfo.print()
print("Container ID: ", containerInfo.id)

print("Moving 'Bird Toys' from 1,1 to 2,0")
calculator.moveContainer(1, 1, 2, 0)
mani.updateManifest(calculator.ship_bay_array)
mani.printManifest()
containerInfo = calculator.ship_bay_array[2][0]
print(f"Container Info: ")
containerInfo.print()