SELECT CD_Prj_ODR_Check.ODRID, CD_Prj_ODR_Check.TaskFlowID, CD_Prj_ODR_Check.CheckerID, CD_Prj_ODR_Check.CheckResult, CD_TaskTrack.RoundNo
FROM CD_TaskSource
INNER JOIN CD_TaskTrack ON CD_TaskTrack.TaskID = CD_TaskSource.ID
INNER JOIN CD_Prj_ODR_Check ON CD_Prj_ODR_Check.ODRID = CD_TaskSource.SourceID
Limit 100;