Var
    FilePath    :   TDynamicString;
    DescList    :   TStringList;
    AllFootprintName            :  TStringList;
    AllDesc                     :  TStringList;
    WorkSpace                   :  IWorkSpace;
    Project                     :  IProject;
    j,k                           :  Integer;
    Document                    :  IDocument;
    CurrentLib                  :  IPCB_Library;
    LibComp                     :  IPCB_LibComponent;
    LibraryIterator             :  IPCB_LibraryIterator;
    CompIsFoundList             :  TStringList;
    Messager                    :  IMessagesManager;


Procedure OpenFile;
Var
   Res  :  String;

Begin
     ResetParameters;
     AddStringParameter('Dialog', 'FileOpenSave');
     AddStringParameter('Mode' , '0');
     AddStringParameter('FileType1' , 'Comma Separated Values (*.csv)|*.csv');
     RunProcess('Client:RunCommonDialog');

     GetStringParameter('Result' , Res);
     If (Res = 'True') Then
     Begin
         GetStringParameter('Path' , FilePath);
         //ShowMessage(FilePath);
     End;
End;


Procedure RemoveQuotationInDesc;
Var i,p :   Integer;
Begin
     For i := 0 to AllDesc.Count -1 Do
     Begin
          p := Pos('"',AllDesc[i]);
          If p = 1 Then
          Begin
          AllDesc[i] := Copy(AllDesc[i], 2, Length(AllDesc[i]) - 2);    //delete a couple of quotation
          End;
     End;
End;

Procedure LoadDescList;
Var
   p, i      :            Integer;

Begin
     DescList := TStringList.Create;
     AllFootprintName := TStringList.Create;
     AllDesc := TStringList.Create;
     DescList.LoadFromFile(FilePath);

     If DescList.Count = 0 Then
          ShowMessage('Please check source data');

     For i := 0 to DescList.Count -1 Do
     Begin
         p := Pos(',' , DescList[i]);
         AllFootprintName.Add(Copy(DescList[i], 1, p -1));  // get left part of string
         AllDesc.Add(Copy(DescList[i], p + 1, Length(DescList[i]) - p + 1));      // get right part of string
     End;
End;


Procedure SetCompDesc;
Begin
     LibraryIterator := CurrentLib.LibraryIterator_Create;
     LibraryIterator.SetState_FilterAll;
     LibComp := LibraryIterator.FirstPCBObject;
     While LibComp <> Nil Do
     Begin
          For k := 0 To AllFootprintName.Count -1 Do
          Begin
               If LibComp.Name = AllFootprintName[k] Then
               Begin

               CompIsFoundList[k] := 'True';

               PCBServer.SendMessageToRobots(LibComp.I_ObjectAddress, c_Broadcast, PCBM_BeginModify,c_NoEventData);
               LibComp.Description := AllDesc[k];
               PCBServer.SendMessageToRobots(LibComp.I_ObjectAddress, c_Broadcast, PCBM_EndModify , c_NoEventData);
               CurrentLib.RefreshView;
               PCBServer.RefreshDocumentView(CurrentLib.Board.FileName);
               End;
          End;

          LibComp := LibraryIterator.NextPCBObject;
     End;

     CurrentLib.LibraryIterator_Destroy(LibraryIterator);
End;



Procedure GetPCBlib;
Begin
     WorkSpace := GetWorkSpace;
     Project := WorkSpace.DM_FocusedProject;
     For j := 0 To Project.DM_LogicalDocumentCount - 1 Do
     Begin
          Document := Project.DM_LogicalDocuments(j);
          If Document.DM_DocumentKind = 'PCBLIB' Then
          Begin
               CurrentLib := Client.OpenDocument('PCBLIB' , Document.DM_FullPath);
               Client.ShowDocument(CurrentLib);
               CurrentLib := PCBServer.GetCurrentPCBLibrary;
               SetCompDesc;
          End;
     End;
End;



Procedure InitIsFoundList;
Var i :   Integer;
Begin
     CompIsFoundList := TStringList.Create;
     For i := 0 To AllFootprintName.Count - 1 Do
     Begin
          CompIsFoundList.Add('False');
     End;
End;


Procedure freeMemory;
Begin
     DescList.Free;
     AllFootprintName.Free;
     AllDesc.Free;
     CompIsFoundList.Free;
End;


Procedure NotFoundReport;
Var
    i :   Integer;
    MessageCount : Integer;
Begin
     Messager := WorkSpace.DM_MessagesManager;
     Messager.ClearMessages;
     Messager.BeginUpdate;
     MessageCount := 0;
     For i := 0 to  CompIsFoundList.Count -1 Do
     Begin
          If CompIsFoundList[i] = 'False' Then
          Begin
               Messager.AddMessage('MessageClass 1',
                                   AllFootprintName[i] + ': File not found',
                                   'DXP Message',
                                   'MessageDocument1',
                                   '',
                                   '',
                                   4,
                                   False
               );
               MessageCount := MessageCount + 1;
          End;
     End;
     If MessageCount = 0 Then
        Begin
        Messager.AddMessage('MessageClass 1',
                            'All Description changed',
                            'DXP Message',
                            'MessageDocument1',
                            '',
                            '',
                            3,
                            False
               );
        End;
     Messager.EndUpdate;
     WorkSpace.DM_ShowMessageView;
End;


Procedure GetStart;
Begin
     OpenFile;
     LoadDescList;
     RemoveQuotationInDesc;
     InitIsFoundList;
     GetPCBLib;
     NotFoundReport;
     freeMemory;
End;




