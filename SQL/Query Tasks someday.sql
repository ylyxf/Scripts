SELECT CD_TaskTrack.ID, CD_User.UserName, CD_TaskTrack.TaskNotes FROM CD_TaskTrack
LEFT JOIN CD_User ON CD_User.ID = CD_TaskTrack.UserID
WHERE CD_TaskTrack.EndDate = '20160907';