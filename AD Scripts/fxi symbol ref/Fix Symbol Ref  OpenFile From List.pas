Var
    SymbolList      :          TStringList;
    SymbolRefList   :          TStringList;
    SymbolFileList  :          TStringList;
    AllPathList     :          TStringList;
    FilePath        :          TDynamicString;
    CompIsFoundList :          TStringList;
    j               :          Integer;
    CurrentLib      :          ISCH_Lib;
    LibraryIterator :          ISch_Iterator;
    LibComp         :          ISch_Component;
    WorkSpace       :          IWorkSpace;
    Messager        :          IMessagesManager;
    AView           :          IServerDocumentView;
    AServerDocument :          IServerDocument;

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


Procedure LoadImportedFile;
Var
   p, i      :            Integer;
   TrimedString           :       WideString;

Begin
     SymbolList := TStringList.Create;
     SymbolRefList := TStringList.Create;
     SymbolFileList :=  TStringList.Create;
     AllPathList := TStringList.Create;

     SymbolList.LoadFromFile(FilePath);

     If SymbolList.Count = 0 Then
          ShowMessage('Please check source data');

     For i := 0 to SymbolList.Count -1 Do
     Begin
         p := Pos(',' , SymbolList[i]);
         SymbolFileList.Add(Copy(SymbolList[i], 1, p -1));  // get left part of string
         TrimedString := Copy(SymbolList[i], p + 1, Length(SymbolList[i]) - p + 1); // get right part of string

         p:= Pos(',' , TrimedString);
         SymbolRefList.Add(Copy(TrimedString, 1, p - 1));
         AllPathList.Add(Copy(TrimedString, p + 1, Length(TrimedString) - p + 1));
     End;
End;


Procedure InitIsFoundList;
Var i :   Integer;
Begin
     CompIsFoundList := TStringList.Create;
     For i := 0 To SymbolFileList.Count - 1 Do
     Begin
          CompIsFoundList.Add('False');
     End;
End;



Procedure SetSymbolRef;
Begin
      LibraryIterator := CurrentLib.SchLibIterator_Create;
      LibraryIterator.AddFilter_ObjectSet(MkSet(eSchComponent));
      LibComp := LibraryIterator.FirstSchObject;


            //SchServer.RobotManager.SendMessage(LibComp.I_ObjectAddress, c_BroadCast, SCHM_BeginModify, c_NoEventData);

              LibComp.SymbolReference := SymbolRefList[j];
              LibComp.Comment.Text := '';
              LibComp.ComponentDescription := '';
              LibComp.Designator.Color := 8388608;
              LibComp.Designator.FontID := 1;
              LibComp.Comment.Color :=  8388608;

            //SchServer.RobotManager.SendMessage(LibComp.I_ObjectAddress, c_BroadCast, SCHM_EndModify , c_NoEventData);



      CurrentLib.SchIterator_Destroy(LibraryIterator);
      CurrentLib.GraphicallyInvalidate;
End;


Procedure OpenSCHLibFile;
Begin
     For j := 0 To SymbolFileList.Count - 1 Do
     Begin
          CurrentLib := Client.OpenDocument('SCHLIB' , AllPathList[j] + SymbolFileList[j]);
          If CurrentLib <> Nil Then
          Begin
               Client.ShowDocument(CurrentLib);
               Aview := Client.CurrentView;
               AServerDocument := Aview.OwnerDocument;
               AServerDocument.Modified := True;
               CurrentLib := SCHServer.GetCurrentSchDocument;
               CompIsFoundList[j] := 'True';
               SetSymbolRef;
          End;
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
                                   SymbolFileList[i] + ': File not found',
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
                            'All Symbol changed',
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
     SymbolList.Free;
     SymbolRefList.Free;
     SymbolFileList.Free;
     AllPathList.Free;
     CompIsFoundList.Free;
End;


Procedure GetStart;
Begin
     OpenCSVFile;
     LoadImportedFile;
     InitIsFoundList;
     OpenSCHLibFile;
     NotFoundReport;
     freeMemory;
End;
