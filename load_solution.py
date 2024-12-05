import manifest
import calculate
import load_list_editor

class Tree_Node:
    def __init__(self, array, loader,instruction):
        self.current_array = array
        self.current_list = loader
        self.children = []
        self.instruction = instruction
    
class Load_Solution:
    def __init__(self, array, loader):
        self.manifest_array = array
        self.transfer_list = loader

    def load_instructions(self,manifest_array,loader):
        pass
        #check if is_finished

        #generate successors
        #each successor is the result of a single instruction and contains said instruction within it

        #go down one successor

        #return true if solution is found
        #return false if solution is not found

    def is_finished(self, current_transfer_list):
        containers_left = 0
        for key in current_transfer_list.pending_loads:
            containers_left += current_transfer_list.pending_loads[key]
        
        for key in current_transfer_list.offload_list:
            containers_left += current_transfer_list.offload_list[key]

        if(containers_left == 0):
            return True
        else:
            return False
    
    def is_in_offloads(self,current_transfer_list,container):
        if container.container_description in self.offload_list:
            return True
        else
            return False

    