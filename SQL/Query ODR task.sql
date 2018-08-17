SELECT CD_TaskTrack.TaskID, CD_User.UserName, CD_TaskTrack.EffortTime, CD_TaskTrack.EndTime, CD_TaskTrack.RoundNo, CD_TaskTrack.TaskNotes FROM CD_TaskTrack
INNER JOIN CD_TaskSource ON CD_TaskSource.ID = CD_TaskTrack.TaskID
INNER JOIN CD_User ON CD_User.ID = CD_TaskTrack.UserID
WHERE CD_TaskSource.TaskFlowID = 51
AND CD_TaskTrack.EndTime > '2016-04-10'
S;