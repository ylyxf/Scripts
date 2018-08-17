__author__ = 'frank.qiu'


import csv

def readCSVinDict(filePath):
    csvData = open(filePath, "rU")
    dataDictList = list(csv.DictReader(csvData))

    return dataDictList

def getRootManufacturer(manufDataAll, manuf):
    if manuf["parentid"] == "NULL":
        return "NULL"

    currentManuf = manuf
    parentFound = 0
    while currentManuf["parentid"] != "NULL":
        for previousManuf in manufDataAll:
            if previousManuf["manufacturerid"] == currentManuf["manufacturerid"]:
                continue

            if previousManuf["manufacturerid"] == currentManuf["parentid"]:
                currentManuf = previousManuf
                parentFound = 1

        if  not parentFound: return "NULL"

    return currentManuf

manufacturers =readCSVinDict(r"G:\Scripts\Python\Manufacturer Data\manufacturer table.csv")
manufacturerAlias = readCSVinDict(r"G:\Scripts\Python\Manufacturer Data\manufacturer alias table.csv")

manufacturersAndAlias = {}
for manuf in manufacturers:
    if manuf["parentid"] == "NULL":
        if not manufacturersAndAlias.has_key(manuf["manufacturerid"]):
            manufacturerData = {}
            manufacturerData["name"] = manuf["name"]
            manufacturerData["alias"] = []
            manufacturersAndAlias[manuf["manufacturerid"]] = manufacturerData

for manuf in manufacturers:
    if manuf["parentid"] != "NULL":
        rootManuf = getRootManufacturer(manufacturers, manuf)

        if rootManuf != "NULL":
            manufacturersAndAlias[rootManuf["manufacturerid"]]["alias"].append(manuf["name"])

for manufAlia in manufacturerAlias:
    #print manufAlia
    if manufAlia["parentid"] != "NULL":
        rootManuf = getRootManufacturer(manufacturers, manuf)

        if rootManuf != "NULL":
            manufacturersAndAlias[rootManuf["manufacturerid"]]["alias"].append(manuf["name"])


print manufacturersAndAlias["3002"]