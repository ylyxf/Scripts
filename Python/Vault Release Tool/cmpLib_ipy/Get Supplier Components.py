from cmpLib_ipy import *

crPath = "G:\\newcontentteam\\Components\\TIRequestSource\\DatabaseLibraries-Marth9thMorning\\done\\Connectors_Sullins.csv"
crType = "TI"

#=============================================================================
if (crType == "Altium"):
    componentSet = parseAluCR(crPath)
else:
    componentSet = parseTIcr(crPath)

supplierComponentsDict = {}
#for component in componentSet.componentList:
    #if component.parmeters

ciivaApi = Ciiva.Apis()
ciivaClient = ciivaApi.GetApiClient()

result = ciivaGetSupplierComponentsBySPN("Digikey", "1-5349580-6-ND", ciivaClient)
for item in xrange(len(result)):
    print result[item]["Description"]
print result