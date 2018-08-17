SELECT CD_TaskSource.SourceID as 'ODRID', CD_TaskTrack.StartTime, CD_TaskTrack.EndTime, CD_TaskTrack.EffortTime, CD_Prj_ODR.IsTaskDone as 'DeviceDone', CD_TaskTrack.UserID, CD_TaskTrack.TaskNotes, CD_Prj_ODR.Deadline
FROM CD_TaskSource
INNER JOIN CD_TaskTrack ON CD_TaskTrack.TaskID = CD_TaskSource.ID
INNER JOIN CD_Prj_ODR On CD_Prj_ODR.ID = CD_TaskSource.SourceID
WHERE CD_TaskTrack.EndDate > 20160411
AND CD_Prj_ODR.ProjectId = 1

