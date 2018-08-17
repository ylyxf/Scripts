var
    FilePath        :          TDynamicString;
    CurrentLib      :          ISCH_Lib;
    LibraryIterator :          ISch_Iterator;
    LibComp         :          ISch_Component;
    WorkSpace       :          IWorkSpace;
    Messager        :          IMessagesManager;
    PinIterator     :          ISch_Iterator;
    CurrentPin      :          ISch_Pin;
    ReportList      :          TStringList;
    PinLocationX    :          Integer;
    PinLocationY    :          Integer;
    i               :          Integer;

Procedure OpenSchLib;
Var
   Res    :          String;

Begin
     ResetParameters;
     AddStringParameter('Dialog', 'FileOpenSave');
     AddStringParameter('Mode' , '0');
     AddStringParameter('FileType1' , 'Schematic Library(*.schlib)|*.schlib');
     RunProcess('Client:RunCommonDialog');

     GetStringParameter('Result' , Res);
     If (Res = 'True') Then
     Begin
         GetStringParameter('Path' , FilePath);
     End
     else exit;

     CurrentLib := Client.OpenDocument('SCHLIB', FilePath);
     Client.ShowDocument(CurrentLib);
     CurrentLib := SCHServer.GetCurrentSchDocument;

     ReportList := TStringList.Create;

     LibraryIterator := CurrentLib.SchLibIterator_Create;
     LibraryIterator.AddFilter_ObjectSet(MkSet(eSchComponent));
     LibComp := LibraryIterator.FirstSchObject;

     While LibComp <> Nil do
     Begin
          PinIterator := LibComp.SchIterator_Create;
          PinIterator.AddFilter_ObjectSet(MkSet(ePin));
          CurrentPin := PinIterator.FirstSchObject;

          While CurrentPin <> Nil do
          Begin
               PinLocationX := CurrentPin.Location.X div 100000;
               PinLocationY := CurrentPin.Location.Y div 100000;

               If (((PinLocationX + 10) mod 10 <> 0) or ((PinLocationY + 10) mod 10 <> 0)) Then
               Begin
                    ReportList.Add(CurrentPin.OwnerSchComponent.SymbolReference + ': Pin ' + CurrentPin.Designator + ' (' + IntToStr(PinLocationX) + ' , ' + IntToStr(PinLocationY) + ')');
               End;

               CurrentPin := PinIterator.NextSchObject;
          End;

          LibComp.SchIterator_Destroy(PinIterator);
          LibComp := LibraryIterator.NextSchObject;
     End;
     CurrentLib.SchIterator_Destroy(LibraryIterator);

     Workspace := GetWorkSpace;
     Messager := Workspace.DM_MessagesManager;
     Messager.ClearMessages;
     Messager.BeginUpdate;

     For i := 0 to ReportList.Count - 1 Do
     Begin
          Messager.AddMessage('Warning',
                              ReportList[i],
                              'Off Grid Checker',
                              CurrentLib.DocumentName,
                              '',
                              '',
                              73,
                              False);
     End;

     If ReportList.Count = 0 Then
     Begin
         Messager.AddMessage('Success',
                            'No pin off grid',
                            'Off Grid Checker',
                            CurrentLib.DocumentName,
                            '',
                            '',
                            3,
                            False
               );
     End;

     Messager.EndUpdate;
     WorkSpace.DM_ShowMessageView;


     ReportList.Free;
End;
