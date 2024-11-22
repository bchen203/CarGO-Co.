


def perform_balance_operation(): #given a 2D array of the manifest, perform the balance operation
    pass

def get_partition(): #Get the partition line (considering which side is left/right)
    pass

def is_balanceable(container_weights, current_weight):
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

        
