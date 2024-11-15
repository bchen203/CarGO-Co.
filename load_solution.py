#import manifest.py

#nabbed from another branch for testing purposes
class Container:
    def __init__(self, container_weight, container_description):
        self.weight = container_weight
        # Note: reserved container names are UNUSED, NAN (will need to check if the operator inputs these names later on)
        self.description = container_description

    def print(self):
        print(f"container weight: {self.weight}")
        print(f"conainer description: {self.description}")


class Loader:
    
    def __init__(self):
        self.pending_loads = []
        self.offload_list = []

    #adds a container from a truck into the load list
    def add_load(self,name,weight):
        truck_container = Container(weight,name)
        self.pending_loads.append(truck_container)

    #prints the load from truck list
    def print_pending_loads(self):
        for truck_container in self.pending_loads:
            print('{} | {} kg'.format(truck_container.description, truck_container.weight))
    
    #removes a container from load from truck list
    def remove_pending_loads(self,index):
        self.pending_loads.pop(index)

    #returns pending_loads
    def get_pending_loads(self):
        return self.pending_loads



    #adds a container from the ship into the offload list
    def add_offload(self,name,weight):
        ship_container = Container(weight,name)
        self.offload_list.append(ship_container)

    #prints the offload from ship list
    def print_offload_list(self):
        for ship_container in self.offload_list:
            print('{} | {} kg'.format(ship_container.description, ship_container.weight))
    
    #removes a container from offload from ship list
    def remove_offload_list(self,index):
        self.offload_list.pop(index) 
        #MIGHT NEED TO CHANGE IMPLEMENTATION BECAUSE CONTAINER SELECTED ON GRID MAY NOT CORRESPOND
        #TO CONTAINER SELECTED FOR INSTRUCTION IN THE CASE OF DUPLICATE CONTAINERS
    
    #returns offload_list
    def get_offload_list(self):
        return self.offload_list
    
if __name__ == "__main__":
        transfer = Loader()
        transfer.add_offload("James", 40)
    
        transfer.print_offload_list()

    
    


