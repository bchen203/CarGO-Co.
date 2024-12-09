import sys
sys.path.append('../CargoCo')
import calculate
import manifest

test_manifest = manifest.Manifest("SampleManifests/ShipCase1.txt")
ship_case1, v = test_manifest.copyManifest()

#TEST 1 get_top_container function - should return false (empty column)
print("TEST 1")
test_container = calculate.get_top_container(ship_case1,3)

if(test_container):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 2 get_top_container function - should return false (column with only 'NAN')
print("TEST 2")
test_container = calculate.get_top_container(ship_case1,11)

if(test_container):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 3 get_top_container function - returns a container
print("TEST 3")
test_container = calculate.get_top_container(ship_case1,1)

if(test_container):
    print("Test Passed!")
else:
    print("Test Failed!")

#TEST 4 get_supported_empty_space function - should return false (entirely filled column)
print("TEST 4")
test_manifest4 = manifest.Manifest("SampleManifests/ShipCase4.txt")
ship_case4, v = test_manifest4.copyManifest()
test_container = calculate.get_supported_empty_space(ship_case4,4)

if(test_container):
    print("Test Failed!")
else:
    print("Test Passed!")

#TEST 5 get_supported_empty_space function - should return 'UNUSED' container (position is above y = 0)
print("TEST 5")
test_container = calculate.get_supported_empty_space(ship_case4,0)
if(test_container):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 6 get_supported_empty_space function - should return 'UNUSED' container (position is y = 0)
print("TEST 6")
test_container = calculate.get_supported_empty_space(ship_case1,3)
if(test_container):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 7 get_time - returns correct time (start pos is 8,0)
print("TEST 7")
time_sum = calculate.get_time(8,0,0,0)
if(time_sum == 10):
    print("Test Passed!")
else:
    print("Test Failed!")

#TEST 8 get_time - returns correct time (end pos is 8,0)
print("TEST 8")
time_sum = calculate.get_time(0,0,8,0)
if(time_sum == 10):
    print("Test Passed!")
else:
    print("Test Failed!")
#TEST 9 get_time - returns correct time (neither pos is 8,0)
print("TEST 9")
time_sum = calculate.get_time(1,2,3,4)
if(time_sum == 4):
    print("Test Passed!")
else:
    print("Test Failed!")