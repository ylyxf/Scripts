SELECT a.ID FROM CD_Prj_ODR a JOIN CD_TaskSource b ON a.ID=b.SourceID and b.TaskFlowID=51 
WHERE not Exists(SELECT 1 FROM CD_Symbol c WHERE c.TaskID=b.ID) and Not Exists(SELECT 1 FROM CD_Footprint c WHERE c.TaskID=b.ID)
AND a.id IN (1)