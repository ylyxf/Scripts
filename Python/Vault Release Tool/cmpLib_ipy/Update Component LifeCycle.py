from cmpLib_ipy import *
#this script doesn't work so far. a released revision in vault can't be modified in below way
#so the property LifeCycelStatus can't be updated. Need to research if there is other way 
config = configInfo()
config.readConfigFile("Config.ini")

vaultAddress = config.configDict["Vault Adddress"]
userName = config.configDict["User Name"]
pwd = config.configDict["Password"]

client = initVaultConnection(vaultAddress, userName, pwd)

cmpName = "INA3221AIRGVT"
contentTypeGUID = "CB3C11C4-E317-11DF-B822-12313F0024A2"
queryStr = "Comment = '%s' AND ContentTypeGUID = '%s'" %(cmpName, contentTypeGUID)
print queryStr
#options = VaultSDK.VaultRequestOptions()
#options.Add(VaultSDK.VaultRequestOption.IncludeAllItemRevisions)
itemRevisions = client.GetItemRevisions(queryStr)

#find max revID for each item revision
revisionIdCheck = {}
for itemRevision in itemRevisions:
    if revisionIdCheck.has_key(itemRevision.ItemGUID):
        if revisionIdCheck[itemRevision.ItemGUID] < itemRevision.RevisionId: 
            revisionIdCheck[itemRevision.ItemGUID] = itemRevision.RevisionId 
    else:
        revisionIdCheck[itemRevision.ItemGUID] = itemRevision.RevisionId 

#add latest revsion into list
itemRevisionsLatest = []
for itemRevision in itemRevisions:
    if itemRevision.RevisionId == revisionIdCheck[itemRevision.ItemGUID]:
        itemRevisionsLatest.append(itemRevision)

for lastestRevision in itemRevisionsLatest:
    pushLifeCycleStateToNext(lastestRevision, client)