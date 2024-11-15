import time
from datetime import datetime
import pytz


#Global Variables
la = pytz.timezone('America/Los_Angeles')
utc = pytz.timezone('UTC')
logFileName = "" #in format 'KeoghsPort[YEAR].txt
lastOperatorName = None

#Helpers:


#Base functions
def addTimePrefix(logMessage):
    #UTC time
    currentTime = datetime.now(utc)
    local_time = currentTime.astimezone(la)

    #Truncation:
    time_prefix = local_time.strftime("%Y-%m-%d %H:%M:%S")
    return f"{time_prefix} {logMessage}"

def generateFileName():
    currentTime = datetime.now(utc)
    local_time = currentTime.astimezone(la)

    currentYear = local_time.strftime("%Y")

    return f"KeoghsPort{currentYear}.txt"

def writeToLogFile(logMessage):
    #Open Log, write to it, close file again
    with open(logFileName, "a+") as logFile:
        logFile.write(logMessage)
        logFile.write("\n")

def writeToLogSafe(logMessage):
    messageWithPrefix = addTimePrefix(logMessage)
    global logFileName 
    logFileName= generateFileName()

    #TODO sanitize any inputs with non-ascii
    writeToLogFile(messageWithPrefix)

#Each log:
def logOperatorSignIn(operatorName):
    global lastOperatorName
    if not lastOperatorName == None:
        writeToLogSafe(f"{lastOperatorName} signs out")
    
    writeToLogSafe(f"{operatorName} signs in")
    lastOperatorName = operatorName
        
def logOperatorComment(logMessage):
    
    
    pass

def logLoadUnloadOperation(containerName, isLoad):
    pass

def logBalanceOperation(shipName, isSift):
    pass

def logFinishCycle(shipName):
    pass

def logEndOfYearShutdown():
    #Remember to set OperatorName to None
    pass

#testing:
# writeToLogSafe("TestMessageAgain")
# print(addTimePrefix("Special comment example"))
# print(generateFileName())

def testCase(shipName, containerNameSample):
    
    #Testing filename:
    print("Test 1: ", generateFileName() == "KeoghsPort2024.txt")

    #TestingTimePrefix:
    print("Test 2: ", addTimePrefix("TestMessage"))

    #testing Write to file:
    try:
        writeToLogSafe("SampleMessage")
        print("Test 3: Write to file passed")
    except:
        print("Test 3 Failed: Write to file failed")

    #Operator signin / out:
    try:
        logOperatorSignIn("Allison Burgers")
        print("Test 4: Operator signin with no previous operator works")
    except:
        print("Test 4 Failed: Operator signin with no previous operator works")

    try:
        #Another signin/out, with a previous operator:
        logOperatorSignIn("Jamilton Snagwich")
        print("Test 5: Operator signing with previous operator works")
    except:
        print("Test 5 Failed: Operator signing with previous operator works")
        

    #Operator Comment:
    

        
    
        


testCase("ShipeName", "Walmart Toys")

