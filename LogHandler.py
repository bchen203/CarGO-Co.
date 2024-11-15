import time
from datetime import datetime
import pytz


#Global Variables
la = pytz.timezone('America/Los_Angeles')
utc = pytz.timezone('UTC')
logFileName = "" #in format 'KeoghsPort[YEAR].txt

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
    pass

def logOperatorComment(logMessage):
    pass

def logLoadUnloadOperation(containerName, isLoad):
    pass

def logBalanceOperation(shipName, isSift):
    pass

def logFinishCycle(shipName):
    pass

def logEndOfYearShutdown():
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
    writeToLogSafe("SampleMessage")


testCase("ShipeName", "Walmart Toys")

