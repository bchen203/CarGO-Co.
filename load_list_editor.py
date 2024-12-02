import manifest


class Loader:
    
    def __init__(self):
        self.pending_loads = {}
        self.offload_list = {}

    #adds a container from a truck into the load list
    def add_pending_load(self,name):

        if name in self.pending_loads:
            self.pending_loads[name] = self.pending_loads[name] + 1
        else:
            self.pending_loads[name] = 1

    #prints the load from truck list
    #not called by the gui
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
        if name in self.offload_list:
            self.offload_list[name] = self.offload_list[name] + 1
        else:
            self.offload_list[name] = 1

    #prints the offload from ship list
    #not called by the gui
    def print_offload_list(self):
        for key in self.offload_list:
            print('{} | {}'.format(key, self.offload_list[key]))
    
    #removes a container from offload from ship list
    def remove_offload_list(self,name):
        if self.offload_list[name] > 0:
            self.offload_list[name] = self.offload_list[name] - 1

    #returns offload_list
    def get_offload_list(self):
        return self.offload_list
    
if __name__ == "__main__":
        
        #Test 1: Adding new container names to Pending Loads List
        print("\nTest 1: Adding new container names to pending loads list")
        pending = Loader()
        pending.add_pending_load("Henry Space Age Toys")
        pending.add_pending_load("Money Robin Dee Banks")
    
        if "Henry Space Age Toys" in pending.pending_loads and "Money Robin Dee Banks" in pending.pending_loads:
            print("Test Passed")
        else:
            print("Test Failed")

        #Test 2: Adding existing container name to Pending Loads List
        print("\nTest 2: Adding existing container name to pending loads list")
        pending.add_pending_load("Henry Space Age Toys")

        if pending.pending_loads["Henry Space Age Toys"] == 2:
            print("Test Passed")
        else:
            print("Test Failed")
        
        print("\nPrintout of pending loads list:")
        pending.print_pending_loads()
        #Test 3: Removing existing container name for Pending Loads List
        print("\nTest 3: Removing existing container name for pending loads list")
        pending.remove_pending_loads("Money Robin Dee Banks")

        if not "Money Robin Dee Banks" in pending.pending_loads:
            print("Test Passed")
        else:
            print("Test Failed")


        #Test 4: Removing one instance of a container name with duplicates for Pending Loads List
        print("\nTest 4: Removing one instance of a container name with duplicates for pending loads list")
        pending.remove_pending_loads("Henry Space Age Toys")
        if pending.pending_loads["Henry Space Age Toys"] == 1:
            print("Test Passed")
        else:
            print("Test Failed")

        #Test 5: Get Pending Dictionary
        print("\nTest 5: Getting pending dictionary")
        pend_dictionary = pending.get_pending_loads()
        if pend_dictionary["Henry Space Age Toys"] == 1:
            print("Test Passed")
        else:
            print("Test Failed")

#      offloader.add_offload("Dallas Moon Shoes")
#       offloader.add_offload("Tungsten Cubes")

        #Test 6: Adding new container names to Loading Loads List
        print("\nTest 6: Adding new container names to loading loads list")
        loading = Loader()
        loading.add_offload("Dallas Moon Shoes")
        loading.add_offload("Tungsten Cubes")
    
        if "Dallas Moon Shoes" in loading.offload_list and "Tungsten Cubes" in loading.offload_list:
            print("Test Passed")
        else:
            print("Test Failed")

        #Test 7: Adding existing container name to Loading Loads List
        print("\nTest 7: Adding existing container name to loading loads list")
        loading.add_offload("Dallas Moon Shoes")

        if loading.offload_list["Dallas Moon Shoes"] == 2:
            print("Test Passed")
        else:
            print("Test Failed")

        print("\nPrintout of offloads list:")
        loading.print_offload_list()
        
        #Test 8: Removing existing container name for Loading Loads List
        print("\nTest 8: Removing existing container name for loading loads list")
        loading.remove_offload_list("Tungsten Cubes")

        if loading.offload_list["Tungsten Cubes"] == 0:
            print("Test Passed")
        else:
            print("Test Failed")


        #Test 9: Removing one instance of a container name with duplicates for Loading Loads List
        print("\nTest 9: Removing one instance of a container name with duplicates for loading loads list")
        loading.remove_offload_list("Dallas Moon Shoes")
        if loading.offload_list["Dallas Moon Shoes"] == 1:
            print("Test Passed")
        else:
            print("Test Failed")

        #Test 10: Get Loading Dictionary
        print("\nTest 10: Getting loading dictionary")
        load_dictionary = loading.get_offload_list()
        if load_dictionary["Dallas Moon Shoes"] == 1:
            print("Test Passed")
        else:
            print("Test Failed")

    
    


