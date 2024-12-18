import manifest


class Loader:
    
    def __init__(self, loads_list={}, offloads_list={}):
        self.pending_loads = loads_list
        self.offload_list = offloads_list

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
    


