from cmpLib_ipy import *

#vaultAddress = "http://vault.live.altium.com"
#userName = "frank.qiu@altium.com"
#pwd = "123456"
#folderPath = "Unified Components/Components/Texas Instruments/Models/PCB Components"
vaultAddress = "http://shavault01.altium.biz:9780"
userName = "admin"
pwd = "admin"
folderPath = "Components/TI Components/Models/Footprints"
report = "G:\\repo.txt"

client = initVaultConnection(vaultAddress, userName, pwd)
allfolders = getVaultFolders(client)

print "getting models"
modelList = getItemInfoinSpeificFolder(folderPath, client, allfolders)
f = open(report, "wb")
for model in modelList:
    print model.Comment
    f.write(model.Comment + "|" + model.HRID + "|" + model.ItemGUID + "|" + model.RevisionGUID)
    f.write("\r\n")