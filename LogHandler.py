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

def getLogContents():
    with open(logFileName) as logFile:
        logContents = logFile.read()
    return logContents

#Each log:
def logOperatorSignIn(operatorName):
    global lastOperatorName
    if not lastOperatorName == None:
        writeToLogSafe(f"{lastOperatorName} signs out.")
    
    writeToLogSafe(f"{operatorName} signs in.")
    lastOperatorName = operatorName
        
def logOperatorComment(logMessage):
    writeToLogSafe(logMessage)
    pass

def logManifestUpload(shipName, numContainers): #Manifest HMMAlgeciras.txt is opened, there are 12 containers on the ship
    if numContainers == 1:
        writeToLogSafe(f"Manifest {shipName}.txt is opened, there is {numContainers} container on the ship.")
    else:
        writeToLogSafe(f"Manifest {shipName}.txt is opened, there are {numContainers} containers on the ship.")

def logLoadUnloadOperation(containerName, isLoad):
    if isLoad:#Loading: “2024-01-30: 11:08 “Walmart Christmas Cat Toys” is onloaded.”
        writeToLogSafe(f"\"{containerName}\" is onloaded.")
    else:#Offloading: “2024-01-30: 11:08 “Walmart Christmas Cat Toys” is offloaded.
        writeToLogSafe(f"\"{containerName}\" is offloaded.")
    

def logBalanceOperation(shipName, isNotSift):
    if isNotSift: #“2024-1-30: 15:40 Balanced HMSJakartaExplorer within the Maritime Law’s definition of balance.”
        writeToLogSafe(f"Balanced {shipName} within the Maritime Law\'s definition of balance.") 
    else: #2024-1-30: 15:40 HMSThanatos cannot be balanced within Maritime Law’s definition of balance. Balanced ship to match the goal state of SIFT.”
        writeToLogSafe(f"{shipName} cannot be balanced within Maritime Law\'s definition of balance. Balanced ship to match the goal state of SIFT.")

def logFinishCycle(shipName):
    writeToLogSafe(f"Finished a Cycle. Manifest {shipName}OUTBOUND.txt was written to desktop, and a reminder pop-up to operator to send file was displayed.")

def logEndOfYearShutdown():
    #Remember to set OperatorName to None
    global lastOperatorName
    
    writeToLogSafe(f"{lastOperatorName} shuts down Mr. Keogh's Port for the year, and {lastOperatorName} signs out.")
    # writeToLogSafe(f"{lastOperatorName} signs out.")

    lastOperatorName = None #to prevent signout message when re-opening port

    pass
