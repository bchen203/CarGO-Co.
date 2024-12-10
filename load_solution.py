import manifest
import calculate
import load_list_editor
import heapq
class Tree_Node:
    def __init__(self, array, loader,instruction,parent,instruction_num):
        self.current_array = array #state of the manifest
        self.current_list = loader #transfer list minus already completed directions
        self.instruction = instruction #last instruction that results in the current state of manifest
        self.parent = parent # parent tree node
        self.instruction_num = instruction_num

#TO DO LIST:
#convert it to a class
#paramater - one should be a calculate class
#paramater - one should store an instruction list
#make a start function that makes load_instruction easier to call
#change load_instructions() to return a list of instructions, rather than list of Tree_Nodes

#root node has no instruction and no parent
#instruction num of -1
def load_instructions(root_node): #should output a list of INSTRUCTIONS
    successor_number = 0
    cost = 0
    unvisited_nodes = [(cost,successor_number,root_node)]
    successor_number += 1
    heapq.heapify(unvisited_nodes)
    once = 1
    visited_nodes = []
    #check if is_finished
    while(unvisited_nodes):
        current_cost,v,current_node = unvisited_nodes[0]
        unvisited_nodes.pop(0)

        if(is_finished(current_node)):
            #MAKE THE LIST OF NODES/INSTRUCTIONS THAT IS CORRECT
            current_instruction_num = current_node.instruction_num
            node_list = set()
            while(current_instruction_num >= 0):
                node_list[current_instruction_num] = current_node
                current_node = current_node.parent
                current_instruction_num -= 1
            return node_list #returns list of nodes which in order, contains every instruction and array state


        for start_column in range(12): #selecting starting pos
            start_space = get_top_container(current_node.current_array,start_column)
            if(start_space != False):
                if(once):
                    print('{},{},{} start space'.format(start_space.y,start_space.x,start_space.description))
                for dest_column in range(12): #selecting end pos
                    
                    if(start_column != dest_column):
                        end_space = get_supported_empty_space(current_node.current_array,dest_column)
                        if(end_space != False):
                            #creating a successor with an instruction moves a container within ship
                            #ADD DOUBLE CHECKING THAT ARRAY STATE IS NOT REPEATED
                            successor_array = current_node.current_array.copy()
                            calculator = calculate.Calculate(successor_array,0)

                           # if(once):
                            #    print('{},{} goes to {},{}'.format(start_space.y,start_space.x,end_space.y,end_space.x))
                            calculator.moveContainer(start_space.y,start_space.x,end_space.y,end_space.x)
                            successor_instruction = calculate.Instruction(0,(start_space.y,start_space.x),(end_space.y,end_space.x)  )
                            successor = Tree_Node(successor_array,current_node.current_list,successor_instruction,current_node,current_node.instruction_num + 1)
                            successor_cost = get_time(start_space.y,start_space.x,end_space.y,end_space.x)
                            if(not is_repeated_move(successor,visited_nodes)):
                                heapq.heappush(unvisited_nodes,(current_cost + successor_cost,successor_number,successor))
                                successor_number += 1

                #creating successor moving from ship to truck (only requires a start_column)
                #end pos for a ship to truck pos is (8,0)
                
                if(start_space in current_node.current_list.offload_list):
                    successor_array = current_node.current_array.copy()
                    calculator = calculate.Calculate(successor_array,0)
                    calculator.offloadContainer(start_space.y,start_space.x)
                    successor_instruction = calculate.Instruction(0,(start_space.y,start_space.x),(8,0))
                    successor_list = current_node.current_list.copy()
                    successor_list.remove_offload_list(start_space.description)
                    successor = Tree_Node(successor_array,successor_list,successor_instruction,current_node,current_node.instruction_num + 1)
                    successor_cost = get_time(start_space.y,start_space.x,8,0)
                    heapq.heappush(unvisited_nodes,(current_cost + successor_cost,successor_number,successor))
                    successor_number += 1
        
        #creating a successor where we move a container from truck to ship
        '''
        for dest_column in range(0,12):
            end_space = get_supported_empty_space(current_node.current_array,dest_column)
            container_to_load = get_truck_container(current_node.current_list)
            if(end_space != False):
                successor_array = current_node.current_array.copy()
                calculator = calculate.Calculate(successor_array,0)
                calculator.loadContainer(container_to_load,end_space.y,end_space.x)
                successor_instruction = calculate.Instruction(0,(8,0),(end_space.y,end_space.x))
                successor_list = current_node.current_list.copy()
                successor_list.remove_pending_loads(container_to_load)
                successor = Tree_Node(successor_array,successor_list,successor_instruction,current_node,current_node.instruction_num + 1)
                successor_cost = get_time(8,0,end_space.y,end_space.x)
                heapq.heappush(unvisited_nodes,(current_cost+successor_cost,successor_number,successor) )
                successor_number += 1
        '''
        #stuff after making all the successors
        visited_nodes.append(current_node)

        #TEST STUFF
        if(once):
            for unvisited in unvisited_nodes:
                unvisited_instruction = unvisited[2].instruction
               # print('{} goes to {}'.format(unvisited_instruction.starting_location, unvisited_instruction.ending_location))
            once = 0

    return False #for when no solution is possible (should probably never happen)


                            




   



#looks at the transfer list and checks whether we are in finished state
def is_finished(tree_node):
    containers_left = 0
    for key in tree_node.current_list.pending_loads:
        containers_left += tree_node.current_list.pending_loads[key]
    
    for key in tree_node.current_list.offload_list:
        containers_left += tree_node.current_list.offload_list[key]

    if(containers_left == 0):
        return True
    else:
        return False

#checks if a given container is in the current offloads list
def is_in_offloads(current_transfer_list,container):
    if container.description in current_transfer_list.offload_list:
        return True
    else:
        return False

#checks if the current tree node's array matches any visited nodes' array (duplicate checking)
def is_repeated_move(tree_node,visited_nodes):
    for node in visited_nodes:
        visited_array = node.current_array
        is_identical = True
        for row in range(8):
            for column in range(12):
                if tree_node.current_array[row][column].description != visited_array[row][column].description:
                    is_identical = False

        if(is_identical):
            return True
    return False

#inside the column of an array, returns topmost container
def get_top_container(array,column):
    current_row = 7
    while(current_row >= 0):
        
        if array[current_row][column].description == "UNUSED":
            pass 
            #when current location is empty
        elif array[current_row][column].description == "NAN":
            #print("returned NAN")
            return False
            #when current space has NAN
            #idk figure out a way to make it work
        else:
            #print("returned container")
            return array[current_row][column]
        current_row -= 1
    #print("returned unused")
    return False
    

#finds a suitable destination space (returns container class with 'UNUSED') for a container in a given column
def get_supported_empty_space(array,column):
    current_row = 7
    while(current_row >= 0):
        if array[current_row][column].description == "UNUSED":
            pass 
            #when current location is empty
        else:
            if(current_row < 7):
                return array[current_row+1][column]
            else:
                return False
        current_row -= 1

    return array[0][column]
    #when column is empty

#finds the time cost of an instruction
def get_time(startRow,startCol,endRow,endCol):
    time = 0
    if(startRow == 8 and startCol == 0):
        time += 2 #time to move from ship to truck
    elif(endRow == 8 and endCol == 0):
        time += 2 #time to move from truck to ship

    time += abs(startRow-endRow) + abs(startCol-endCol)
    return time

#gets the name of a container that needs to be moved from truck to ship
def get_truck_container(transfer_list):
    load_list = transfer_list.get_pending_loads()
    if(load_list):
        for key in load_list:
            return key
    else:
        return False


#TESTING THE SUBFUNCTIONS
arr = [[manifest.Container(0, "UNUSED", -1, r, c) for c in range(12)] for r in range(8)]
list = load_list_editor.Loader()
list.add_offload("Cory Luggage")
instruction = calculate.Instruction(0,(0,0),(0,1))
test_node = Tree_Node(arr,list,instruction,None,0)

#TEST 1 is_finished function - should return false
print("TEST 1")
if is_finished(test_node):
    print("Test Failed!")
else:
    print("Test Passed!")

test_node.current_list.remove_offload_list("Cory Luggage")
test_node.current_list.add_pending_load("Poe Packings")

if is_finished(test_node):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 2 is_finished function - should return true
print("TEST 2")
test_node.current_list.remove_pending_loads("Poe Packings")
if is_finished(test_node):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 3 is_in_offloads function - should return false
print("TEST 3")
test_container = manifest.Container(0,"Mini Marshmallow Moths",0,0,0)
if is_in_offloads(test_node.current_list,test_container):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 4 is_in_offloads function - should return true
print("TEST 4")
test_node.current_list.add_offload("Mini Marshmallow Moths")
if is_in_offloads(test_node.current_list,test_container):
    print("Test Passed!")
else:
    print("Test Failed!")

#TEST 5 is_repeated_move function - should return false
print("TEST 5")
test_visited_nodes = []
if is_repeated_move(test_node,test_visited_nodes):
    print("Test Failed!")
else:
    print("Test Passed!")

test_manifest = manifest.Manifest("SampleManifests/ShipCase1.txt")
ship_case1, v = test_manifest.copyManifest()

second_node = Tree_Node(ship_case1,list,instruction,None,0)
test_visited_nodes.append(second_node)

if is_repeated_move(test_node,test_visited_nodes):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 6 is_repeated_move function - should return true
print("TEST 5")
test_visited_nodes.append(second_node)
if is_repeated_move(second_node,test_visited_nodes):
    print("Test Passed!")
else:
    print("Test Failed!")

ship_case1[1][2].changeWeight(5)
third_node = Tree_Node(ship_case1,list,instruction,None,0)
if is_repeated_move(third_node,test_visited_nodes):
    print("Test Passed!")
else:
    print("Test Failed!")

#TEST 7 get_top_container function - should return false (empty column)
print("TEST 7")
test_container = get_top_container(ship_case1,3)

if(test_container):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 8 get_top_container function - should return false (column with only 'NAN')
print("TEST 8")
test_container = get_top_container(ship_case1,11)

if(test_container):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 9 get_top_container function - returns a container
print("TEST 9")
test_container = get_top_container(ship_case1,1)

if(test_container):
    print("Test Passed!")
else:
    print("Test Failed!")

#TEST 10 get_supported_empty_space function - should return false (entirely filled column)
print("Test 10")
test_manifest4 = manifest.Manifest("SampleManifests/ShipCase4.txt")
ship_case4, v = test_manifest4.copyManifest()
test_container = get_supported_empty_space(ship_case4,4)

if(test_container):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 11 get_supported_empty_space function - should return 'UNUSED' container (position is above y = 0)
print("Test 11")
test_container = get_supported_empty_space(ship_case4,0)
if(test_container):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 12 get_supported_empty_space function - should return 'UNUSED' container (position is y = 0)
print("Test 12")
test_container = get_supported_empty_space(ship_case1,3)
if(test_container):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 13 get_time - returns correct time (start pos is 8,0)
print("Test 13")
time_sum = get_time(8,0,0,0)
if(time_sum == 10):
    print("Test Passed!")
else:
    print("Test Failed!")

#TEST 14 get_time - returns correct time (end pos is 8,0)
print("Test 14")
time_sum = get_time(0,0,8,0)
if(time_sum == 10):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 15 get_time - returns correct time (neither pos is 8,0)
print("Test 15")
time_sum = get_time(1,2,3,4)
if(time_sum == 4):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 16 get_truck_container - returns a container name
list = load_list_editor.Loader()
list.add_pending_load("Very Heavy Rocks")
if get_truck_container(list):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 17 get_truck_container- returns false (empty list)
list = load_list_editor.Loader()
if get_truck_container(list):
    print("Test Failed!")
else:
    print("Test Passed!")

#ACTUAL TESTS FOR THE LOAD SOLUTION
#THE MEAT
#TEST 18 load_instruction - already solved array
testing_manifest = manifest.Manifest("SampleManifests/ShipCase1.txt")
testing_list = load_list_editor.Loader()
testing_node = Tree_Node(testing_manifest.copyManifest(),testing_list, None,None,-1 )

instruction_list = load_instructions(testing_node)
if(instruction_list):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 19 load_instruction - needs to unload one thing

testing_manifest = manifest.Manifest("SampleManifests/ShipCase1.txt")
testing_manifest.printManifest()
testing_array = testing_manifest.copyManifest()[0].copy()
#print(len(testing_array))
testing_list = load_list_editor.Loader()
testing_list.add_offload("Cat")
testing_node = Tree_Node(testing_array,testing_list, None,None,-1 )

instruction_list = load_instructions(testing_node)
if(instruction_list):
    print("Test Passed!")
else:
    print("Test Failed!")