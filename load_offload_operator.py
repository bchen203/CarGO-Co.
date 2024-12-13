import manifest
import calculate
import heapq



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
        
        
        self.instructionList = solution_array

        return solution_array

    def perform_load_offload_operation_uniform_cost(self, manifest_array,loader):
        #Need a heapqueue that has tuples (Total Time, [Array of instructions])
        instruction_heap = []
        #curId = self.get_highest_id(self.calculator.ship_bay_array)
        #print(curId)
        heapq.heappush(instruction_heap, (0, [])) 
   
        
        while(True): #break on finding a solution
            current_state = heapq.heappop(instruction_heap)
            
            curInstructionTime = current_state[0]
            curInstructionsArray = current_state[1]
           
            
            for instruction in curInstructionsArray: #applying current instructions, will need to reverse after
                self.follow_instruction(instruction,loader)

            if self.is_finished_transferring(loader): #break if complete
                reverseInstructions = list(curInstructionsArray)
                reverseInstructions.reverse()
                for instruction in reverseInstructions:
                    self.follow_reverse_instruction(instruction,loader)
                return curInstructionsArray
            
           # if(self.get_highest_id(self.calculator.ship_bay_array) >= curId):
           #     curId = self.get_highest_id(self.calculator.ship_bay_array)

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
                        curInstruction = calculate.Instruction(0,(8,0),(container.y,container.x))
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
    
    #finds current highest id in array
    def get_highest_id(self,array):
        id = 0
        for row in range(8):
            for col in range(12):
                if(array[row][col].id > id):
                    id = array[row][col].id
        return id
        
    def follow_instruction(self,instruction,loader,):
       
        if(instruction.starting_location[0] == 8 and instruction.starting_location[1] == 0): 
            #instruction is load
            

            current_container = manifest.Container(-1,self.get_truck_container(loader),-1, instruction.ending_location[0], instruction.ending_location[1])
            
            
            self.loading_stack.append(current_container)
            loader.remove_pending_loads(current_container.description)
            #print("loading: %s", current_container.description)
            self.calculator.loadContainer(current_container.description,instruction.ending_location[0], instruction.ending_location[1])
            current_container.id = self.calculator.ship_bay_array[instruction.ending_location[0]][instruction.ending_location[1]].id
            instruction.container_id = current_container.id
            
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
            self.calculator.containerID = self.calculator.containerID - 1
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


   