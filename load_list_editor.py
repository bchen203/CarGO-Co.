#import manifest.py

#nabbed from another branch for testing purposes
class Container:
    def __init__(self, container_weight, container_description):
        self.weight = container_weight
        # Note: reserved container names are UNUSED, NAN (will need to check if the operator inputs these names later on)
        self.description = container_description

    def print(self):
        print(f"container weight: {self.weight}")
        print(f"container description: {self.description}")


class Loader:
    
    def __init__(self):
        self.pending_loads = []
        self.offload_list = []

    #adds a container from a truck into the load list
    def add_pending_load(self,name,weight):
        shown_weight = 0
        if(weight < 0):
            shown_weight = 0
        elif(weight > 99999 ):
            shown_weight = 99999
        else:
            shown_weight = weight
        
        shown_weight = round(shown_weight)

        truck_container = Container(shown_weight,name)
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
        shown_weight = 0
        if(weight < 0):
            shown_weight = 0
        elif(weight > 99999 ):
            shown_weight = 99999
        else:
            shown_weight = weight
        
        shown_weight = round(shown_weight)

        ship_container = Container(shown_weight,name)
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
        
        #Test 1: Adding to Pending Loads List
        print("\nTest 1:")
        pending = Loader()
        pending.add_pending_load("Henry Space Age Toys", 40)
        pending.add_pending_load("Money Robin Dee Banks", 800)
    
        pending.print_pending_loads()

        #Test 2: Removing from Pending Loads List
        print("\nTest 2:")
        pending.remove_pending_loads(0)

        pending.print_pending_loads()
        
        #Test 3: Getting the Pending Loads List
        print("\nTest 3:")
        pending_list = pending.get_pending_loads()
        pending_list.pop().print()


        #Test 4: Edge Cases for Adding to Pending Loads List
        print("\nTest 4:")
        pending.add_pending_load("Dallas Moon Shoes", -80)
        pending.add_pending_load("Tungsten Cubes", 999999)
        pending.add_pending_load("Dessie Decibel Speakers", 40.567)

        pending.print_pending_loads()

        #Test 5: Adding to Offload List
        print("\nTest 5:")
        offloader = Loader()
        offloader.add_offload("Henry Space Age Toys", 40)
        offloader.add_offload("Money Robin Dee Banks", 800)
    
        offloader.print_offload_list()

        #Test 6: Removing from Offload List
        print("\nTest 6:")
        offloader.remove_offload_list(0)

        offloader.print_offload_list()
        
        #Test 7: Getting the Offload List
        print("\nTest 7:")
        offload_list = offloader.get_offload_list()
        offload_list.pop().print()


        #Test 8: Edge Cases for Adding to the Offload List
        print("\nTest 8:")
        offloader.add_offload("Dallas Moon Shoes", -80)
        offloader.add_offload("Tungsten Cubes", 999999)
        offloader.add_offload("Dessie Decibel Speakers", 40.567)

        offloader.print_offload_list()
    
    


