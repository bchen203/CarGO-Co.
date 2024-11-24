


def perform_balance_operation(): #given a 2D array of the manifest, perform the balance operation
    pass

#Will return a solution
def perform_balance_operation_brute_force_helper(current_left_containers, current_right_containers, current_weight, remaining_containers): #recursive brute force :')
    
    #base case
    if len(remaining_containers) == 0:
        if is_balanced(current_weight[0], current_weight[1]):
            return (current_left_containers, current_right_containers) #Insert correct solution, where each container is sorted to left or right
        else:
            return None
    else:
        if is_balanceable(remaining_containers, current_weight):
            current_container = remaining_containers.pop()

            #Left
            new_left_containers = current_left_containers
            new_left_containers.append(current_container)
            left = perform_balance_operation_brute_force_helper(new_left_containers, current_right_containers, (current_weight[0]+current_container.weight, current_weight[1]), remaining_containers) 

            #right
            new_right_containers = current_right_containers
            new_right_containers.append(current_container)
            right = perform_balance_operation_brute_force_helper(current_left_containers, new_right_containers, (current_weight[0], current_weight[1]+current_container.weight), remaining_containers) 
            
            if (right == None and not left == None):
                return left
            elif (left == None and not right == None):
                return right
            else:
                return None
        else:
            return None    

def get_partition(array): #Get the partition line (considering which side is left/right) returns last index of left side (inclusive)
    return len(array[0])

def is_balanceable(containers, current_weight): #rewrite container_weights to be a list of containers
    container_weights = []
    for container in containers:
        container_weights.append(container.weight)

    sorted_weights = sorted(container_weights)
    for container in sorted_weights:
        if current_weight[0] > current_weight[1]:
            current_weight[1] += container
        else:
            current_weight[0] += container

    if (is_balanced(current_weight[0], current_weight[1])):
        return True
    else:
        return False

def is_balanced(port_weight, starboard_weight):

    return (max(port_weight, starboard_weight) / min(port_weight , starboard_weight) < 1.1)

def is_ship_balanced(manifest_array):
    
    #Adding all the port weights to port, and adding all the starboard weights to starboard, then running is_balanced
    pass

        
