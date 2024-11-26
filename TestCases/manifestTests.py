import manifest

fileName = "SampleManifests/ShipCase1.txt"

# __________invalid file input name__________
try:
  importedFile = open(fileName, "r")
except:
  print(f"[ERROR] Could not open file {fileName}.")

theManifest = manifest.Manifest(fileName)

grid = theManifest.copyManifest()
theManifest.printManifest()



# __________confirm that the format is correct in the exported manifest__________
theManifest.exportManifest()
try:
  exportedFileName = fileName[:-4] + "OUTBOUND.txt"
  exportedFile = open(exportedFileName, "r")
except:
  print(f"[ERROR] Could not open file {exportedFileName}.")

inFile = importedFile.read()
outFile = exportedFile.read()

assert inFile == outFile, "[ERROR] Input manifest does not match output manifest"



# Test cases:
# [DONE] invalid file input name
# floating/invalid location for container
# moving/offloading unused or nan slots
# loading a container onto a nan slot
# uploading a non .txt file
# uploading a .txt file formatted incorrectly
#   use regex to check
# [DONE] confirm that the format is correct in the exported manifest
#   Do this by inputting a manifest, perform zero operations, then export the outbound manifest
#   The outbound manifest should match the input manifest exactly