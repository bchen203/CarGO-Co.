import sys
sys.path.append('../CargoCo')
import LogHandler

#testing:
# writeToLogSafe("TestMessageAgain")
# print(addTimePrefix("Special comment example"))
# print(generateFileName())

def testCase(shipName, containerNameSample):
    
    #Testing filename:
    print("Test 1: ", LogHandler.generateFileName() == "KeoghsPort2024.txt")

    #TestingTimePrefix:
    print("Test 2: ", LogHandler.addTimePrefix("TestMessage"))

    #testing Write to file:
    try:
        LogHandler.writeToLogSafe("SampleMessage")
        print("Test 3: Write to file passed")
    except:
        print("Test 3 Failed: Write to file failed")

    #Operator signin / out:
    try:
        LogHandler.logOperatorSignIn("Allison Burgers")
        print("Test 4: Operator signin with no previous operator works")
    except:
        print("Test 4 Failed: Operator signin with no previous operator fails")

    try:
        #Another signin/out, with a previous operator:
        LogHandler.logOperatorSignIn("Jamilton Snagwich")
        print("Test 5: Operator signing with previous operator works")
    except:
        print("Test 5 Failed: Operator signing with previous operator fails")
        

    #Operator Comment:
    try:
        #Another signin/out, with a previous operator:
        LogHandler.logOperatorComment("I THINK SOMETHING IS WRONG!")
        print("Test 6: Operator signing with previous operator works")
    except:
        print("Test 6 Failed: Operator comment throws an error")

    #Balance Log
    try:
        LogHandler.logBalanceOperation("Dog", True)
        LogHandler.logBalanceOperation("Fake", False)
        print("Test 7: logging balance does not throw an error")
    except:
        print("Test 7 Failed: logging balance fails")
    

    #Load/Unload
    try:
        LogHandler.logLoadUnloadOperation("Cat toys", True)
        LogHandler.logLoadUnloadOperation("Dog Toys", False)
        print("Test 8: logging logging load/offload does not throw an error")
    except:
        print("Test 8 Failed: logging load/offload fails")
    

    #Finish Cycle
    try:
        LogHandler.logFinishCycle("HMSJellyCatJack")
        print("Test 9: Finish Cycle does not throw an error")
    except:
        print("Test 9 Failed: Finish Cycle fails")


    #Shut down port for the year.
    try:
        LogHandler.logEndOfYearShutdown()
        print("Test 10: end of year shutdown does not throw an error")
    except:
        print("Test 10 Failed: end of year shutdown  fails")
    

    #making sure signout works
    try:
        LogHandler.logOperatorSignIn("Haocheng Mai")
        print("Test 11: Signin with no previous operator after a shutdown throws no errors")
    except:
        print("Test 11 Failed: sign-in fails")
    

    
def realisticLog(firstOperator, secondOperator, shipName, containerLoad, containerOffload):
    LogHandler.logOperatorSignIn(firstOperator)
    LogHandler.logManifestUpload(shipName, 15)
    LogHandler.logLoadUnloadOperation(containerLoad, True)
    LogHandler.logLoadUnloadOperation(containerOffload, False)
    LogHandler.logFinishCycle(shipName)
    

    newShipName = shipName + "ButAwesome"
    LogHandler.logOperatorSignIn(secondOperator)
    LogHandler.logManifestUpload(newShipName, 40)
    LogHandler.logBalanceOperation(newShipName, False)
    LogHandler.logFinishCycle(newShipName)
    LogHandler.logEndOfYearShutdown()


realisticLog("Zachary Snackary", "Haocheng Mai", "HMSJellycatJack", "Walmart Boxes", "Walmart Polygonal Toy")
testCase("ShipeName", "Walmart Toys")