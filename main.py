from azure.storage.blob import *
import sys

# Usage function
def helpUsage():
    print("Usage: python main.py -s storageAccountName -k key -c [containers] -f fileType")
    sys.exit(69)

print("Welcome to the storage utility. Shows you blobs of a certain file type in each container you provide!")
print("Usage: python main.py -s storageAccountName -k key -c [containers] -f fileType")
print("Args from command line are: ")
print(sys.argv)

marker = None
SAName = ""
SAKey = ""
fileType = ""
containers = []
blobsList = []
totalSize = 0

# help section
for arg in sys.argv:
    if arg == "help":
        helpUsage()
for arg in sys.argv:
    if arg == "h":
        helpUsage()
for arg in sys.argv:
    if arg == "-help":
        helpUsage()
for arg in sys.argv:
    if arg == "-h":
        helpUsage()

for x in range(len(sys.argv)):
    if sys.argv[x] == "-s":
        SAName = sys.argv[x+1]
    if sys.argv[x] == "-k":
        SAKey = sys.argv[x+1]
    if sys.argv[x] == "-f":
        fileType = sys.argv[x+1]
    if sys.argv[x] == "-c":
        for y in range(x+1, len(sys.argv)):
            if sys.argv[y] == "-s":
                break
            if sys.argv[y] == "-f":
                break
            if sys.argv[y] == "-k":
                break
            else:
                containers.append(sys.argv[y])

print("The containers are: ")
print(containers)
print("     The Storage account is: " + SAName)
print("     The key is: " + SAKey)
print("     The file type for search is: " + fileType)

block_blob_service = BlockBlobService(account_name=SAName, account_key=SAKey)
serviceContainers = block_blob_service.list_containers()

for c in serviceContainers:
    print("     " + c.name + ":")
    blobs = block_blob_service.list_blobs(c.name, marker=marker)
    blobsList.extend(blobs)
    for blob in blobsList:
        blob_property = BlockBlobService.get_blob_properties(block_blob_service, c.name, blob.name)
        if str(blob_property.name).endswith(fileType):
            print(blob_property.name + ": " + str(blob_property.properties.content_length) + " bytes")
            totalSize += blob_property.properties.content_length
print("Total size of " + fileType + " files: " + str(totalSize) + " bytes")
