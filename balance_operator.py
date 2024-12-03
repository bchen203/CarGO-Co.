import manifest
import calculate


def perform_balance_operation(manifest_array): #given a 2D array of the manifest, perform the balance operation
    # First: Check if already balanced
    is_ship_balanced(manifest_array)

    # Second: Calculate the solution
    left = []
    right = []
    current_weight = [0,0]
    remaining_containers = []
    goal_position = perform_balance_operation_brute_force_helper(left, right, current_weight, remaining_containers)
    
    # Third: which goal state will be easiest to achieve (which side will be side 1, which side will be side 2?)
    # Might need to skip this for now

    # Fourth: Figuring out where to place the containers
    partition = get_partition()
    for container in goal_position[0]:
        pass

    container_move_instructions = generate_container_moves(goal_position[0], goal_position[1])

    # Fifth: Making the moves (updating 2D array through calculate.py)
    for instruction in container_move_instructions:
        #TODO: Add function call to update 2D array in calculate
        pass

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
    return len(array[0])/2

#Given a list of containers and a tuple with the left and right side weights, figure out if everything is still sortable in the current state
def is_balanceable(containers, current_weight): 
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

# Given a left-side and right-side weight, returns True if balanced, False if not balanced.
def is_balanced(port_weight, starboard_weight):

    return (max(port_weight, starboard_weight) / min(port_weight , starboard_weight) < 1.1)

#Checks if a ship is balanced
def is_ship_balanced(manifest_array): #manifest is a 2D array
    left_partition_inclusive = get_partition(manifest_array) 

    port_weight = 0
    starboard_weight = 0

    for row in manifest_array: #assumign row-column?
        i = 0
        for container in row:
            #skip if not a container (IE NAN or UNUSED)

            if i <= left_partition_inclusive:
                port_weight += container.weight
            else:
                starboard_weight_weight += container.weight
            i += 1
    
    return is_balanced(port_weight, starboard_weight)   

def get_side(container, manifest_array):

    partition = get_partition(manifest_array)

    #TODO: return 'left' or 'right' strings depending on container location
    # Look into whether contaienrs have a position attached to them
     


#Returns a list of moves, provided left-side and right-side arrays with containers.
def generate_container_moves(left_containers, right_containers): 
    

    # some early thoughts:
    #  - Prioritize top / higher containers
    #  - Prioritize placing containers with as few moves as possible (ie, nearer to the middle)
    #  - Avoid placing contaienrs on top of other contaienrs that need to be moved.
    # Will need helper function to help with figuring out if a container is already on the left/right


    


    
    pass