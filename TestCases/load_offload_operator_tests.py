import sys
sys.path.append('../CargoCo')

import load_offload_operator
import calculate
import manifest
import load_list_editor

#Test 1: Run operator with empty Loader
print("Test 1: Run operator with empty Loader")
mani = manifest.Manifest("SampleManifests/ShipCase1.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])

operator = load_offload_operator.Load_Offload_Operator(calculator)

load_offload_list = load_list_editor.Loader()
result_instructions = operator.perform_load_offload_operation(manifest_info[0],load_offload_list)


if(result_instructions == []):
    print("Test Passed")
else:
    print("Test Failed")

'''
load_offload_list.add_offload("Cat")
load_offload_list.remove_offload_list("Cat")
if operator.is_finished_transferring(load_offload_list):
    print("Yes")
else:
    print("No")
'''
#Test 2: Run operator with Loader with a single offload to do
print("Test 2: Run operator with Loader with a single offload to do")
mani = manifest.Manifest("SampleManifests/ShipCase1.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])

operator = load_offload_operator.Load_Offload_Operator(calculator)

load_offload_list = load_list_editor.Loader()
load_offload_list.add_offload("Cat")
result_instructions = operator.perform_load_offload_operation(manifest_info[0],load_offload_list)

if(result_instructions[0].starting_location == (0,1)):
    print("Test Passed")
else:
    print("Test Failed")

#Test 3: Run operator with Loader with a single offload and a single load
print("Test 3: Run operator with Loader with a single offload and a single load to do")
mani = manifest.Manifest("SampleManifests/ShipCase1.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])

operator = load_offload_operator.Load_Offload_Operator(calculator)
load_list = {}
offload_list = {}
offload_list = dict((description, dupes) for description, dupes in offload_list.items() if dupes > 0)
load_offload_list = load_list_editor.Loader(load_list,offload_list)
load_offload_list.add_offload("Cat")
load_offload_list.add_pending_load("Sheep")
operator.is_finished_transferring(load_offload_list)
result_instructions = operator.perform_load_offload_operation(manifest_info[0],load_offload_list)

for instruction in result_instructions:
    pass
    #instruction.print()
if(len(result_instructions) == 2):
    print("Test Passed")
else:
    print("Test Failed")

#Test 4: Run operator with Loader with a single offload with many containers above it
print("Test 4: Run operator with Loader with a single offload with many containers above it")
mani = manifest.Manifest("SampleManifests/ShipCase4.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])

operator = load_offload_operator.Load_Offload_Operator(calculator)
load_list = {}
offload_list = {}
offload_list = dict((description, dupes) for description, dupes in offload_list.items() if dupes > 0)
load_offload_list = load_list_editor.Loader(load_list,offload_list)
load_offload_list.add_offload("Dog")
result_instructions = operator.perform_load_offload_operation(manifest_info[0],load_offload_list)

for instruction in result_instructions:
    pass
    #instruction.print()
if(len(result_instructions) == 6):
    print("Test Passed")
else:
    print("Test Failed")

#Test 5: Run operator with Loader with a completely full manifest requiring one load and offload
print("Test 5: Run operator with Loader with a completely full manifest requiring one load and offload")
mani = manifest.Manifest("SampleManifests/ShipCaseFull.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])

operator = load_offload_operator.Load_Offload_Operator(calculator)
load_list = {}
offload_list = {}
offload_list = dict((description, dupes) for description, dupes in offload_list.items() if dupes > 0)
load_offload_list = load_list_editor.Loader(load_list,offload_list)
load_offload_list.add_pending_load("Worthy Edge Razors")
load_offload_list.add_offload("James")
result_instructions = operator.perform_load_offload_operation(manifest_info[0],load_offload_list)

for instruction in result_instructions:
    pass
    #instruction.print()
if((len(result_instructions) == 2)):
    print("Test Passed")
else:
    print("Test Failed")

#Test 6: Run operator with Loader with a completely empty  manifest requiring 4 loads
print("Test 6: Run operator with Loader with a completely empty  manifest requiring 4 loads")
mani = manifest.Manifest("SampleManifests/ShipCaseEmpty.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])

operator = load_offload_operator.Load_Offload_Operator(calculator)
load_list = {}
offload_list = {}
offload_list = dict((description, dupes) for description, dupes in offload_list.items() if dupes > 0)
load_offload_list = load_list_editor.Loader(load_list,offload_list)
load_offload_list.add_pending_load("Worthy Edge Razors")
load_offload_list.add_pending_load("Wright Brothers Model Planes")
load_offload_list.add_pending_load("Fey Cosplay Molding Clay")
load_offload_list.add_pending_load("Larry's Statues")
result_instructions = operator.perform_load_offload_operation(manifest_info[0],load_offload_list)

for instruction in result_instructions:
    pass
    #instruction.print()
if((len(result_instructions) == 4)):
    print("Test Passed")
else:
    print("Test Failed")


#Test 7: Run operator with Case 6 from Dr. Keogh's email (Silver Queen)
print("Test 7: Run operator with Case 6 from Dr. Keogh's email (Silver Queen)")
mani = manifest.Manifest("SampleManifests/SilverQueen.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])

operator = load_offload_operator.Load_Offload_Operator(calculator)
load_list = {}
offload_list = {}
offload_list = dict((description, dupes) for description, dupes in offload_list.items() if dupes > 0)
load_offload_list = load_list_editor.Loader(load_list,offload_list)
load_offload_list.add_pending_load("Natron")
load_offload_list.add_offload("Batons")
load_offload_list.add_offload("Catfish")
result_instructions = operator.perform_load_offload_operation(manifest_info[0],load_offload_list)

for instruction in result_instructions:
    pass
    #instruction.print()
if((len(result_instructions) == 4)):
    print("Test Passed")
else:
    print("Test Failed")
    