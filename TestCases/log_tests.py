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
        print("Test 4 Failed: Operator signin with no previous operator works")

    try:
        #Another signin/out, with a previous operator:
        LogHandler.logOperatorSignIn("Jamilton Snagwich")
        print("Test 5: Operator signing with previous operator works")
    except:
        print("Test 5 Failed: Operator signing with previous operator works")
        

    #Operator Comment:

    #Balance Log
    LogHandler.logBalanceOperation("Dog", True)
    LogHandler.logBalanceOperation("Fake", False)

    #Load/Unload
    LogHandler.logLoadUnloadOperation("Cat toys", True)
    LogHandler.logLoadUnloadOperation("Dog Toys", False)

    #Finish Cycle
    LogHandler.logFinishCycle("HMSJellyCatJack")

    #Shut down port for the year.
    LogHandler.logEndOfYearShutdown()

    #making sure signout works
    LogHandler.logOperatorSignIn("Haocheng Mai")

    
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