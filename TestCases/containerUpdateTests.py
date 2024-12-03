import sys
sys.path.append('../CargoCo')
import manifest
# import calcuate





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
print(f"Manifest array: ")
mani.printManifest()
print("Container: ")
manifest_array[coordinate_1[0]][coordinate_1[1]].print()

print(f"Testing Coordinate 2: {coordinate_2}")
print(f"Manifest array: ")
mani.printManifest()
print("Container: ")
manifest_array[coordinate_2[0]][coordinate_2[1]].print()
