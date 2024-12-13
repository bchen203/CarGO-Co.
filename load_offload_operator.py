import manifest
import calculate
import heapq

#TODO: Change the implementation of global variables

class Load_Offload_Operator():

    def __init__(self, calculator):
        self.calculator = calculator
        self.instructionList = []
        self.loading_stack = []
        self.offloading_stack = []

    def perform_load_offload_operation(self, manifest_array,loader): #given a 2D array of the manifest, perform the load/offload operation
        # First: Check if there are no loads or offloads to be done
        if (self.is_finished_transferring(loader)):
            return [] #empty set of instructions

        #First-Point-Five: Check if the load/offload operation is possible
        if (not self.is_load_offload_possible(manifest_array,loader)):
            return None

        # Second: Calculate the solution
        solution_array = self.perform_load_offload_operation_uniform_cost(self.calculator.ship_bay_array,loader)
        
        # Third: Making the moves (updating 2D array through calculate.py)
        # for instruction in solution_array:
        #     self.calculator.moveContainer(instruction.starting_location[0], instruction.starting_location[1], instruction.ending_location[0],  instruction.ending_location[1])
        #     pass
        self.instructionList = solution_array

        return solution_array

    def perform_load_offload_operation_uniform_cost(self, manifest_array,loader):
        #Need a heapqueue that has tuples (Total Time, [Array of instructions])
        instruction_heap = []
        
        heapq.heappush(instruction_heap, (0, [])) #Getting started, I'd like to write it so that the loop can handle it w/o special setup

    # First, check if balanced (done in the function that calls this)
    # Then, explore every single possible move, generating an instruction and pushing that and it's total time to the heapqueue
    # For each tuple in the heapqueue, do the following loop:
    # Pop move with least time. A
    # Apply imstructions to the grid based on the list of instructions
    # Find all possible moves, push all of them to the heapqueue, based on the old list of instructions
    # Move on
        
        while(True): #break on finding a solution
            current_state = heapq.heappop(instruction_heap)
            
            curInstructionTime = current_state[0]
            curInstructionsArray = current_state[1]
            #print(curInstructionTime)
            
            for instruction in curInstructionsArray: #applying current instructions, will need to reverse after
                self.follow_instruction(instruction,loader)

            if self.is_finished_transferring(loader): #break if balanced
                reverseInstructions = list(curInstructionsArray)
                reverseInstructions.reverse()
                for instruction in reverseInstructions:
                    self.follow_reverse_instruction(instruction,loader)
                return curInstructionsArray

            is_offload_possible_now = 0
            #Find each possible move, from each possible container:
            movable_containers = []
            for column in range(len(self.calculator.ship_bay_array[0])):
                curContainer = calculate.get_top_container(self.calculator.ship_bay_array, column)
                if not curContainer == False: #False if none in that column
                    movable_containers.append(curContainer)

            for container in movable_containers:
                if(self.is_in_offloads(loader,container)):
                    is_offload_possible_now = 1

            if(is_offload_possible_now):
                for container in movable_containers:
                    if(self.is_in_offloads(loader,container)): #for offloads
                        #print("offload time")
                        curInstruction = calculate.Instruction(container.id, (container.y,container.x),(8,0))
                        instructionTime = calculate.get_time(curInstruction.starting_location[0],curInstruction.starting_location[1],8,0)
                        newInstructions = list(curInstructionsArray)
                        newInstructions.append(curInstruction)
                        heapq.heappush(instruction_heap, (curInstructionTime + instructionTime, newInstructions)) #Pushing updated time and instruction array.
                       # print(curInstructionTime + instructionTime)
            else:
                load_destinations = []
                for column in range(len(self.calculator.ship_bay_array[0])):
                    if calculate.get_supported_empty_space(self.calculator.ship_bay_array, column) and not self.column_has_offloads(self.calculator.ship_bay_array,loader, column):
                        load_destinations.append(calculate.get_supported_empty_space(self.calculator.ship_bay_array, column) )
                if(self.get_truck_container(loader) and load_destinations != []):
                    for container in load_destinations: #for loads
                        curInstruction = calculate.Instruction(1,(8,0),(container.y,container.x))
                        instructionTime = calculate.get_time(8,0,curInstruction.ending_location[0],curInstruction.ending_location[1])
                        newInstructions = list(curInstructionsArray)
                        newInstructions.append(curInstruction)
                        heapq.heappush(instruction_heap, (curInstructionTime + instructionTime, newInstructions))
                
                else:

                    for container in movable_containers:
                        for column in range(len(self.calculator.ship_bay_array[0])): #for move instructions
                            if container.x == column: #making sure that you cannot put a container on top of itself:
                                continue
                            current_goal_slot = calculate.get_supported_empty_space(self.calculator.ship_bay_array, column)
                            if not current_goal_slot == False: #False if none exists in that column


                                curInstruction = calculate.Instruction(container.id, (container.y, container.x), (current_goal_slot.y, current_goal_slot.x))
                                instructionTime = calculate.get_time(curInstruction.starting_location[0], curInstruction.starting_location[1], curInstruction.ending_location[0], curInstruction.ending_location[1])
                                newInstructions = list(curInstructionsArray)
                                newInstructions.append(curInstruction)
                                #print(container.description)
                                if self.column_has_offloads(self.calculator.ship_bay_array,loader, curInstruction.starting_location[1]):
                                    instructionTime -= 10
                                if self.column_has_offloads(self.calculator.ship_bay_array,loader, curInstruction.ending_location[1]):
                                    instructionTime += 10
                                total_time = (curInstructionTime + instructionTime)+ len(curInstructionsArray)
                                
                                heapq.heappush(instruction_heap, ( total_time, newInstructions)) #Pushing updated time and instruction array.
                            
                
        

               

            #Reversing the changes:
            curInstructionsArray.reverse()
            for instruction in curInstructionsArray:
                self.follow_reverse_instruction(instruction,loader)

            
        pass
    
    def column_has_offloads(self,array,loader,column):
        current_row = 7
        while(current_row >= 0):
            if array[current_row][column].description in loader.offload_list:
                return True
            current_row -= 1
        return False
        

    #checks if load/offload is possible
    def is_load_offload_possible(self,manifest_array,loader):
        num_Offloads = 0
        num_Loads = 0
        offload_list = loader.get_offload_list()
        load_list = loader.get_pending_loads()
        for key in offload_list:
            num_Offloads += offload_list[key]
        for key in load_list:
            num_Loads += load_list[key]
        
        num_occupied = 0
        for row in range(8):
            for col in range(12):
                if(manifest_array[row][col].description != "UNUSED"):
                    num_occupied += 1
        
        return num_occupied + num_Loads - num_Offloads <= 96


        

    #looks at the transfer list and checks whether we are in finished state
    def is_finished_transferring(self,loader):
        containers_left = 0
        for key in loader.pending_loads:
            containers_left += loader.pending_loads[key]
        
        for key in loader.offload_list:
            containers_left += loader.offload_list[key]
        
       
        if(containers_left == 0):
            return True
        else:
            return False
    
    #gets the name of a container that needs to be moved from truck to ship
    def get_truck_container(self,loader):
        load_list = loader.get_pending_loads()
        if(load_list):
            for key in load_list:
                return key
        else:
            return False

    #checks if a given container is in the current offloads list
    def is_in_offloads(self,current_transfer_list,container):
        if container.description in current_transfer_list.offload_list:
            if(current_transfer_list.offload_list[container.description] != 0):
                return True
        
        return False
        
    def follow_instruction(self,instruction,loader):
       
        if(instruction.starting_location[0] == 8 and instruction.starting_location[1] == 0): 
            #instruction is load
            
            current_container = manifest.Container(0,self.get_truck_container(loader),1, instruction.ending_location[0], instruction.ending_location[1])
            self.loading_stack.append(current_container)
            loader.remove_pending_loads(current_container.description)
            print("loading: %s", current_container.description)
            self.calculator.loadContainer(current_container.description,instruction.ending_location[0], instruction.ending_location[1])
            
        elif(instruction.ending_location[0] == 8 and instruction.ending_location[1] == 0): 
            #instruction is offload
            current_container = self.calculator.ship_bay_array[instruction.starting_location[0]][instruction.starting_location[1]]
            self.offloading_stack.append(current_container)
            loader.remove_offload_list(current_container.description)
            #print("offloading: %s", current_container.description)
            self.calculator.offloadContainer(instruction.starting_location[0], instruction.starting_location[1])
           
        else: #instruction is move
            self.calculator.moveContainer(instruction.starting_location[0], instruction.starting_location[1], instruction.ending_location[0], instruction.ending_location[1])

    def follow_reverse_instruction(self,instruction,loader):
        if(instruction.starting_location[0] == 8 and instruction.starting_location[1] == 0):
            #instruction was load so we offload to reverse it
            current_container = self.loading_stack.pop()
            loader.add_pending_load(current_container.description)
            self.calculator.offloadContainer(instruction.ending_location[0], instruction.ending_location[1])
            
        elif(instruction.ending_location[0] == 8 and instruction.ending_location[1] == 0):
            #instruction is offload so we load to reverse it
            current_container = self.offloading_stack.pop()
            loader.add_offload(current_container.description)
            self.calculator.loadContainer(current_container.description,instruction.starting_location[0], instruction.starting_location[1])
           
        else: ##instruction is move so we use another move to reverse it
            self.calculator.moveContainer(instruction.ending_location[0], instruction.ending_location[1], instruction.starting_location[0], instruction.starting_location[1])


    def get_partition(self, array): #Get the partition line (considering which side is left/right) returns last index of left side (inclusive)
        return len(array[0])/2 - 1

    #Given a list of containers and a tuple with the left and right side weights, figure out if everything is still sortable in the current state
    def is_balanceable(self, containers, current_weight): 
        container_weights = []
        for container in containers:
            container_weights.append(container.weight)

        sorted_weights = (sorted(container_weights))
        sorted_weights.reverse()
        
        for container in sorted_weights:
            if current_weight[0] > current_weight[1]:
                current_weight[1] += container
            else:
                current_weight[0] += container

        if (self.is_balanced(current_weight[0], current_weight[1])):
            return True
        else:
            return False

    #Given a manifest, checks whether the ship is balanceable:
    def is_ship_balanceable(self, manifest_array):
        list_of_containers = []

        for row in manifest_array:
            for container in row: 
                if not (container.description == "UNUSED" or container.description ==  "NAN"):
                    list_of_containers.append(container)


        current_weight = [0,0]

        return self.is_balanceable(list_of_containers, current_weight)

    # Given a left-side and right-side weight, returns True if balanced, False if not balanced.
    def is_balanced(self, port_weight, starboard_weight):

        if(port_weight < 1 or starboard_weight < 1): #catching 0 and below
            return False

        return (max(port_weight, starboard_weight) / min(port_weight , starboard_weight) < 1.1)

    #Checks if a ship is balanced
    def is_ship_balanced(self, manifest_array): #manifest is a 2D array
        left_partition_inclusive = self.get_partition(manifest_array) 

        port_weight = 0
        starboard_weight = 0

        for row in manifest_array: #assumign row-column?
            i = 0
            for container in row:
                #skip if not a container (IE NAN or UNUSED)

                if i <= left_partition_inclusive:
                    port_weight += container.weight
                else:
                    starboard_weight += container.weight
                i += 1
        
        return self.is_balanced(port_weight, starboard_weight)   

    #returns instruction list, matching call to load/offload solution
    def get_instruction_list(self):
        #TODO: Add a check for whether a solution has been generated?
        return self.instructionList