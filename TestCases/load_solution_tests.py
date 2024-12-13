import sys
sys.path.append('C:/Users/david/OneDrive/Desktop/CargoCo')
import load_solution
import load_list_editor
import manifest
import calculate

#TESTING THE SUBFUNCTIONS
arr = [[manifest.Container(0, "UNUSED", -1, r, c) for c in range(12)] for r in range(8)]
list = load_list_editor.Loader()
list.add_offload("Cory Luggage")
instruction = calculate.Instruction(0,(0,0),(0,1))
test_node = load_solution.Tree_Node(arr,list,instruction,None,0)

#TEST 1 is_finished function - should return false
print("TEST 1")
if load_solution.is_finished(test_node):
    print("Test Failed!")
else:
    print("Test Passed!")

test_node.current_list.remove_offload_list("Cory Luggage")
test_node.current_list.add_pending_load("Poe Packings")

if load_solution.is_finished(test_node):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 2 is_finished function - should return true
print("TEST 2")
test_node.current_list.remove_pending_loads("Poe Packings")
if load_solution.is_finished(test_node):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 3 is_in_offloads function - should return false
print("TEST 3")
test_container = manifest.Container(0,"Mini Marshmallow Moths",0,0,0)
if load_solution.is_in_offloads(test_node.current_list,test_container):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 4 is_in_offloads function - should return true
print("TEST 4")
test_node.current_list.add_offload("Mini Marshmallow Moths")
if load_solution.is_in_offloads(test_node.current_list,test_container):
    print("Test Passed!")
else:
    print("Test Failed!")

#TEST 5 is_repeated_move function - should return false
print("TEST 5")
test_visited_nodes = []
if load_solution.is_repeated_move(test_node,test_visited_nodes):
    print("Test Failed!")
else:
    print("Test Passed!")

test_manifest = manifest.Manifest("SampleManifests/ShipCase1.txt")
ship_case1, v = test_manifest.copyManifest()

second_node = load_solution.Tree_Node(ship_case1,list,instruction,None,0)
test_visited_nodes.append(second_node)

if load_solution.is_repeated_move(test_node,test_visited_nodes):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 6 is_repeated_move function - should return true
print("TEST 5")
test_visited_nodes.append(second_node)
if load_solution.is_repeated_move(second_node,test_visited_nodes):
    print("Test Passed!")
else:
    print("Test Failed!")

ship_case1[1][2].changeWeight(5)
third_node = load_solution.Tree_Node(ship_case1,list,instruction,None,0)
if load_solution.is_repeated_move(third_node,test_visited_nodes):
    print("Test Passed!")
else:
    print("Test Failed!")

#TEST 7 get_top_container function - should return false (empty column)
print("TEST 7")
test_container = load_solution.get_top_container(ship_case1,3)

if(test_container):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 8 get_top_container function - should return false (column with only 'NAN')
print("TEST 8")
test_container = load_solution.get_top_container(ship_case1,11)

if(test_container):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 9 get_top_container function - returns a container
print("TEST 9")
test_container = load_solution.get_top_container(ship_case1,1)

if(test_container):
    print("Test Passed!")
else:
    print("Test Failed!")

#TEST 10 get_supported_empty_space function - should return false (entirely filled column)
print("Test 10")
test_manifest4 = manifest.Manifest("SampleManifests/ShipCase4.txt")
ship_case4, v = test_manifest4.copyManifest()
test_container = load_solution.get_supported_empty_space(ship_case4,4)

if(test_container):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 11 get_supported_empty_space function - should return 'UNUSED' container (position is above y = 0)
print("Test 11")
test_container = load_solution.get_supported_empty_space(ship_case4,0)
if(test_container):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 12 get_supported_empty_space function - should return 'UNUSED' container (position is y = 0)
print("Test 12")
test_container = load_solution.get_supported_empty_space(ship_case1,3)
if(test_container):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 13 get_time - returns correct time (start pos is 8,0)
print("Test 13")
time_sum = load_solution.get_time(8,0,0,0)
if(time_sum == 10):
    print("Test Passed!")
else:
    print("Test Failed!")

#TEST 14 get_time - returns correct time (end pos is 8,0)
print("Test 14")
time_sum = load_solution.get_time(0,0,8,0)
if(time_sum == 10):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 15 get_time - returns correct time (neither pos is 8,0)
print("Test 15")
time_sum = load_solution.get_time(1,2,3,4)
if(time_sum == 4):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 16 get_truck_container - returns a container name
print("Test 16")
list = load_list_editor.Loader()
list.add_pending_load("Very Heavy Rocks")
if load_solution.get_truck_container(list):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 17 get_truck_container- returns false (empty list)
print("Test 17")
list = load_list_editor.Loader()
if load_solution.get_truck_container(list):
    print("Test Failed!")
else:
    print("Test Passed!")

#ACTUAL TESTS FOR THE LOAD SOLUTION
#THE MEAT
#TEST 18 load_instruction - already solved array
print("Test 18")
testing_manifest = manifest.Manifest("SampleManifests/ShipCase1.txt")
testing_list = load_list_editor.Loader()
testing_node = load_solution.Tree_Node(testing_manifest.copyManifest()[0],testing_list, None,None,-1 )

instruction_list = load_solution.load_instructions(testing_node)
if(instruction_list):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 19 load_instruction - needs to unload one thing
print("Test 19")
testing_manifest = manifest.Manifest("SampleManifests/ShipCase1.txt")
#testing_manifest.printManifest()
testing_array = load_solution.copy.deepcopy(testing_manifest.copyManifest()[0])
testing_list = load_list_editor.Loader()
testing_list.add_offload("Cat")
testing_node = load_solution.Tree_Node(testing_array,testing_list, None,None,-1 )

instruction_list = load_solution.load_instructions(testing_node)

for col in range(8):
    for row in range(12):
        print(instruction_list[0].current_array[col][row].description, end=' ')
    print()

for node in instruction_list:
    node.instruction.print()

if(instruction_list):
    pass
   # print("Test Passed!")
else:
    print("Test Failed!")