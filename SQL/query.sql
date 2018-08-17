select 
  ALU_ItemRevisionStatistic.ItemRevisionGUID,
  ALU_ItemRevisionStatistic.TransactionDatetime,
  IDS.IDS_User.Name as UserName,
  IDS.IDS_Organisation.Name,
  ALU_ItemRevision.HRID,
  ALU_ItemRevision.Comment,
  ALU_ItemRevision.ReleaseDate,
  ALU_ItemRevision.Description,
  ALU_Item.FolderGUID
from ALU_ItemRevisionStatistic 
left join ALU_ItemRevision on ALU_ItemRevision.GUID = ALU_ItemRevisionStatistic.ItemRevisionGUID 
left join ALU_Item on ALU_Item.GUID = ALU_ItemRevision.ItemGUID 
left join IDS.IDS_User on IDS.IDS_User.GUID = ALU_ItemRevisionStatistic.UserGUID 
left join IDS.IDS_Organisation on IDS.IDS_Organisation.GUID = ALU_ItemRevisionStatistic.OrganizationGUID