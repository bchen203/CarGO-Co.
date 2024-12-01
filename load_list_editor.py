import manifest


class Loader:
    
    def __init__(self):
        self.pending_loads = {}
        self.offload_loads = {}

    #adds a container from a truck into the load list
    def add_pending_load(self,name):

        if name in self.pending_loads:
            self.pending_loads[name] = self.pending_loads[name] + 1
        else:
            self.pending_loads[name] = 1

    #prints the load from truck list
    def print_pending_loads(self):
        for key in self.pending_loads:
            print('{} | {}'.format(key, self.pending_loads[key]))
    
    #removes a container from load from truck list
    def remove_pending_loads(self,name):
        self.pending_loads[name] = self.pending_loads[name] - 1
        if self.pending_loads[name] <= 0:
                self.pending_loads.pop(name)

    #returns pending_loads
    def get_pending_loads(self):
        return self.pending_loads



    #adds a container from the ship into the offload list
    def add_offload(self,name):
        if name in self.offload_loads:
            self.offload_loads[name] = self.offload_loads[name] + 1
        else:
            self.offload_loads[name] = 1

    #prints the offload from ship list
    def print_offload_loads(self):
        for key in self.offload_loads:
            print('{} | {}'.format(key, self.offload_loads[key]))
    
    #removes a container from offload from ship list
    def remove_offload_list(self,name):
        if self.offload_loads[name] > 0:
            self.offload_loads[name] = self.offload_loads[name] - 1



    
    #returns offload_list
    def get_offload_loads(self):
        return self.offload_loads
    
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
    
    


