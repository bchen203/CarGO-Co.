import sys
sys.path.append('../CargoCo')
import manifest
import calculate
import balance_operator

#Going to grab some of the test cases provided as an example. For now, writing test cases for the balance solution calculator, will copy over other tests after:
print("Test Case 1: Ship is already Balanced")
mani = manifest.Manifest("SampleManifests/BalanceTestPreBalanced.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])


instructions = balance_operator.perform_balance_operation(calculator.ship_bay_array)
if instructions == []:
    print("TEST PASSED")
else:
    print("Test FAILED")


#Unbalanceable:
print("Test Case 2: Ship is cannot be Balanced (no SIFT yet)")
mani = manifest.Manifest("SampleManifests/BalanceTestUnbalanceable.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])


instructions = balance_operator.perform_balance_operation(calculator.ship_bay_array)
if instructions == None: #will add SIFT later
    print("TEST PASSED")
else:
    print("Test FAILED")


#Test 3 - Balance Cases:
print("Test Case 3: Small expected balancing case")
mani = manifest.Manifest("SampleManifests/BalanceTest1Manifest.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])

instructions = balance_operator.perform_balance_operation(calculator.ship_bay_array)
for instruction in instructions:
    calculator.moveContainer(instruction.starting_location[0], instruction.starting_location[1], instruction.ending_location[0], instruction.ending_location[1])

if balance_operator.is_ship_balanced(calculator.ship_bay_array):  
    print("TEST PASSED")
else:
    print("Test FAILED")


#Test 4:
print("Test Case 4: Small expected balancing case")
mani = manifest.Manifest("SampleManifests/BalanceTest2Manifest.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])

instructions = balance_operator.perform_balance_operation(calculator.ship_bay_array)
for instruction in instructions:
    calculator.moveContainer(instruction.starting_location[0], instruction.starting_location[1], instruction.ending_location[0], instruction.ending_location[1])

if balance_operator.is_ship_balanced(calculator.ship_bay_array):  
    print("TEST PASSED")
else:
    print("Test FAILED")

#Test 5:
print("Test Case 5: Small expected balancing case")
mani = manifest.Manifest("SampleManifests/BalanceTest3Manifest.txt")
manifest_info = mani.copyManifest()
calculator = calculate.Calculate(manifest_info[0], manifest_info[1])

instructions = balance_operator.perform_balance_operation(calculator.ship_bay_array)
for instruction in instructions:
    calculator.moveContainer(instruction.starting_location[0], instruction.starting_location[1], instruction.ending_location[0], instruction.ending_location[1])

if balance_operator.is_ship_balanced(calculator.ship_bay_array):  
    print("TEST PASSED")
else:
    print("Test FAILED")
