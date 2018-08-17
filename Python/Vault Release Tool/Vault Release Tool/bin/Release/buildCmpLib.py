import cmpLib_ipy

vaultAddress = "http://vault.live.altium.com"
cmpLibPath = "G:\\Scripts\\Python\\Vault Release Tool\\Vault Release Tool\\Template.xml"
crPath = "G:\test.csv"
crType = "Altium"
userName = "frank.qiu@altium.com"
pwd = "123456"

cmpLib_ipy.buildCmpLib(crPath, cmpLibPath, crType, vaultAddress, userName, pwd )