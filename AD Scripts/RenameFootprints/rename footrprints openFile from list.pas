Var
    FilePath    :   TDynamicString;
    DescList    :   TStringList;
    AllFootprintName            :  TStringList;
    AllFootprintFile            :  TStringList;
    AllPathList                 :  TStringList;
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


function LastPos(SubStr,MainStr:String):integer;
var
  s: String;
  i,Pos1,Pos2: Integer;
begin
  Result := 0;
  s := '';
  for i := Length(MainStr) downto 1 do
    s := s + MainStr[i];
  Pos1 := Pos(SubStr,s);
  Pos2 := Length(MainStr) - Pos1 + 1;
  Result := Pos2;
end;


Procedure OpenCSVFile;
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
     End;
End;


// the format of CSV file is like:
// Footprint Library File Name    Old PCB name    new PCB name     File path
Procedure LoadImportedFile;
Var
   p, i      :            Integer;
   TrimedString           :       WideString;

Begin
     DescList := TStringList.Create;
     AllFootprintName := TStringList.Create;
     AllDesc := TStringList.Create;
     AllFootprintFile :=  TStringList.Create;
     AllPathList := TStringList.Create;

     DescList.LoadFromFile(FilePath);

     If DescList.Count = 0 Then
          ShowMessage('Please check source data');

     For i := 0 to DescList.Count -1 Do
     Begin
         p := Pos(',' , DescList[i]);
         AllFootprintFile.Add(Copy(DescList[i], 1, p -1));  // get left part of string
         TrimedString := Copy(DescList[i], p + 1, Length(DescList[i]) - p + 1); // get right part of string

         p:= Pos(',' , TrimedString);
         AllFootprintName.Add(Copy(TrimedString, 1, p - 1));
         TrimedString := Copy(TrimedString, p + 1, Length(TrimedString) - p + 1);

         p := LastPos(',' , TrimedString);
         AllDesc.Add(Copy(TrimedString, 1, p - 1));
         AllPathList.Add(Copy(TrimedString, p + 1, Length(TrimedString)- p + 1));
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



Procedure SetCompDesc;
Begin
     LibraryIterator := CurrentLib.LibraryIterator_Create;
     LibraryIterator.SetState_FilterAll;
     LibComp := LibraryIterator.FirstPCBObject;
     While LibComp <> Nil Do
     Begin
          For j := 0 to AllDesc.Count-1 do
          Begin

               If LibComp.Name = AllFootprintName[j] Then
               Begin

                    CompIsFoundList[j] := 'True';

                    PCBServer.SendMessageToRobots(LibComp.I_ObjectAddress, c_Broadcast, PCBM_BeginModify,c_NoEventData);
                    LibComp.Name := AllDesc[j];
                    PCBServer.SendMessageToRobots(LibComp.I_ObjectAddress, c_Broadcast, PCBM_EndModify , c_NoEventData);
                    CurrentLib.RefreshView;
                    PCBServer.RefreshDocumentView(CurrentLib.Board.FileName);
               End;
          End;

          LibComp := LibraryIterator.NextPCBObject;
     End;

     CurrentLib.LibraryIterator_Destroy(LibraryIterator);
End;


Procedure OpenPCBLibFile;
Begin

          CurrentLib := Client.OpenDocument('PCBLIB' , AllPathList[1] + AllFootprintFile[1]);
          If CurrentLib <> Nil Then
          Begin
               Client.ShowDocument(CurrentLib);
               CurrentLib := PCBServer.GetCurrentPCBLibrary;
               SetCompDesc;
          End;

End;


Procedure NotFoundReport;
Var
    i :   Integer;
    MessageCount : Integer;
Begin
     WorkSpace := GetWorkSpace;
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



Procedure freeMemory;
Begin
     DescList.Free;
     AllFootprintName.Free;
     AllDesc.Free;
     CompIsFoundList.Free;
     AllFootprintFile.Free;
     AllPathList.Free;
End;


Procedure GetStart;
Begin
    OpenCSVFile;
    LoadImportedFile;
    InitIsFoundList;
    RemoveQuotationInDesc;
    OpenPCBLibFile;
    NotFoundReport;
    freeMemory;
End;



Procedure testOpen;
Var
  ReportDocument  :  IDocument;
Begin
  ReportDocument  :=  Client.OpenDocument('PCBLIB','G:\FileNded\219-8LPST.PcbLib');
  If  ReportDocument  <>  Nil  Then
  Client.ShowDocument(ReportDocument);
  showMessage(ReportDocument.DM_FileName);
End;

