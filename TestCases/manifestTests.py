import sys
sys.path.append('../CargoCo')
import manifest

def validateInput(fileName):
  print(f"testing {fileName}")
  theManifest = manifest.Manifest(fileName)
  print("test complete\n")

def validateOutboundFormat(fileName):
  print(f"testing {fileName}")
  theManifest = manifest.Manifest(fileName)
  theManifest.exportManifest()

  importedFile = open(fileName, "r")
  exportedFileName = fileName[:-4] + "OUTBOUND.txt"
  exportedFile = open(exportedFileName, "r")

  inFile = importedFile.read()
  outFile = exportedFile.read()
  importedFile.close()
  exportedFile.close()

  if inFile != outFile:
    "[TEST FAILED] Input manifest does not match output manifest"
  print("test complete\n")




print("__________validate file input type & directory__________")

validateInput("SampleManifests/ShipCase1.txt")
validateInput("SampleManifests/ShipCase2.txt")
validateInput("SampleManifests/ShipCase3.txt")
validateInput("SampleManifests/ShipCase4.txt")
validateInput("SampleManifests/ShipCase5.txt")
validateInput("SampleManifests/SilverQueen.txt")
validateInput("SampleManifests/thisFileShouldFail.cpp")
validateInput("NonexistentDirectory/thisFileShouldFail.txt")

print("___________________________________________")



print("__________validate input manifest format__________")

validateInput("SampleManifests/ShipCase1.txt")
validateInput("SampleManifests/ShipCase2.txt")
validateInput("SampleManifests/ShipCase3.txt")
validateInput("SampleManifests/ShipCase4.txt")
validateInput("SampleManifests/ShipCase5.txt")
validateInput("SampleManifests/SilverQueen.txt")
validateInput("SampleManifests/thisFileShouldFail.txt")

print("___________________________________________")



print("__________confirm that the format is correct in the outbound manifest__________")

validateOutboundFormat("SampleManifests/ShipCase1.txt")
validateOutboundFormat("SampleManifests/ShipCase2.txt")
validateOutboundFormat("SampleManifests/ShipCase3.txt")
validateOutboundFormat("SampleManifests/ShipCase4.txt")
validateOutboundFormat("SampleManifests/ShipCase5.txt")
validateOutboundFormat("SampleManifests/SilverQueen.txt")

print("___________________________________________")

#grid = theManifest.copyManifest()
#theManifest.printManifest()



# Test cases:
# [DONE] invalid file input name
# [CALCULATE CLASS] floating/invalid location for container
# [CALCULATE CLASS] moving/offloading unused or nan slots
# [CALCULATE CLASS] loading a container onto a nan slot
# [DONE] uploading a non .txt file
# [DONE] uploading a .txt file formatted incorrectly
#   use regex to check
# [DONE] confirm that the format is correct in the exported manifest
#   Do this by inputting a manifest, perform zero operations, then export the outbound manifest
#   The outbound manifest should match the input manifest exactly