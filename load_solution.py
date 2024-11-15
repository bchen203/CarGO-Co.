#import manifest.py


class Loader:
    def _init_(self,uploaded_manifest)
    self.manifest = uploaded_manifest
    self.load_list = []
    self.offload_list = []

    #adds a container from a truck into the load list
    def add_load(name,weight)
        truck_container = Container(name,weight)
        load_list.append(truck_container)

    #prints the load from truck list
    def print_load_list(self)
        for truck_container in load_list:
            print('{} | {} kg'.format(truck_container.description, truck_container.weight))
    
    #removes a container from load from truck list
    def remove_load_list(index)
        load_list.pop(index)

    #returns load_list
    def get_load_list(self)
        return load_list



    #adds a container from the ship into the offload list
    def add_offload(name,weight)
        ship_container = Container(name,weight)
        offload_list.append(ship_container)

    #prints the offload from ship list
    def print_offload_list(self)
        for ship_container in offload_list:
            print('{} | {} kg'.format(ship_container.description, ship_container.weight))
    
    #removes a container from offload from ship list
    def remove_offload_list(index)
        offload_list.pop(index) 
        #MIGHT NEED TO CHANGE IMPLEMENTATION BECAUSE CONTAINER SELECTED ON GRID MAY NOT CORRESPOND
        #TO CONTAINER SELECTED FOR INSTRUCTION IN THE CASE OF DUPLICATE CONTAINERS
    
    #returns offload_list
    def get_offload_list(self)
        return offload_list

    
    


