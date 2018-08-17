SELECT CD_User.UserName, COUNT(CD_User.UserName) AS TaskCount FROM CD_TaskTrack
LEFT JOIN CD_User ON CD_User.ID = CD_TaskTrack.UserID
WHERE CD_TaskTrack.EndDate > 20160919
GROUP BY CD_User.UserName
ORDER BY TaskCount;