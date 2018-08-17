select cpod.*, cu.username from CD_Prj_ODR_Check  cpod 
JOIN CD_Prj_ODR cpo ON cpo.id=cpod.ODRID
JOIN CD_Device cd on cd.id=cpo.DeviceID
JOIN CD_User cu ON cu.id=cpod.CheckerID
WHERE cd.GenericCode='878321420' and cpod.TaskFlowID=64;