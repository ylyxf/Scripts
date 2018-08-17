//******check rectangle width for TI IC, peer Texas Instruments Altium Designer SchLib Specification.Doc
//******If rectangle width is narrower than 80 mils per character for both horizontal pins
//******at identical Y coordinates and add 300 mils, Rectangle will be wider, the minimum widht is
//******1200 mil.

Var
   WorkSpace    :    IWorkSpace;
   project      :    IProject;
   Document     :    IDocument;
   CurrentLib   :    ISCH_Lib;
   PinCount     :    Integer;
   MaxCount     :    Integer;
   SymbolList   :    TStringList;

Procedure ChangeReport;
Var
    MessageCount : Integer;
    Messager     : IMessagesManager;
    i            : Integer;
Begin
     Messager := WorkSpace.DM_MessagesManager;
     Messager.ClearMessages;
     Messager.BeginUpdate;
     MessageCount := 0;
     For i := 0 to  SymbolList.Count -1 Do
     Begin
          Messager.AddMessage('Message',
                              'Rectangle in Symbol is not wide enough',
                              'AD Script',
                              SymbolList[i],
                              '',
                              '',
                              4,
                              False
                              );
          MessageCount := MessageCount + 1;
     End;
     If MessageCount = 0 Then
        Begin
        Messager.AddMessage('Message',
                            'All Symbols are Fine',
                            'AD Script',
                            'SchLib Library',
                            '',
                            '',
                            3,
                            False
               );
        End;
     Messager.EndUpdate;
     WorkSpace.DM_ShowMessageView;
End;

Procedure CalWidth(PinArray : Isch_Pin, Rectangle : ISch_Rectangle);
Var
   CharacterCount    : Integer;
   i, j, k           : Integer;
   PinName             : WideString;
Begin
     CharacterCount := 0;
     For i := 0 to PinCount - 1 Do
     Begin
          CharacterCount := 0;
          For j := 0 to PinCount - 1 Do
          Begin
               If (PinArray[i].Location.y = PinArray[j].Location.y)
                   and (PinArray[i].Location.x <> PinArray[j].Location.x)
                   and (PinArray[i].OwnerPartDisplayMode = PinArray[j].OwnerPartDisplayMode)
                   and (PinArray[i].OwnerPartId = Rectangle.OwnerPartId)
                   and (PinArray[j].OwnerPartId = Rectangle.OwnerPartId)  Then
               Begin
                    PinName :=   PinArray[i].Name;
                    for k := 1 to  Length(PinName) Do
                    Begin
                         If PinName[k] <> '\' Then CharacterCount := CharacterCount + 1;
                    End;

                    PinName :=   PinArray[j].Name;
                    for k := 1 to  Length(PinName) Do
                    Begin
                         If PinName[k] <> '\' Then CharacterCount := CharacterCount + 1;
                    End;
                   
                    If MaxCount < CharacterCount Then MaxCount := CharacterCount;
               End;
          End;
     End;

End;

Procedure WideSymbol(PinArray : Isch_Pin; Rectagnle : Isch_Rectangle);
Var
   SymbolWidth : Integer;
   i           : Integer;
   Location    : Tlocation;
Begin
     SymbolWidth := (MaxCount*800000 + 3000000);
     SymbolWidth := ((SymbolWidth Div 2000000) + 1) * 2000000;
     If SymbolWidth < 11000000 Then SymbolWidth := 11000000;
     SchServer.RobotManager.SendMessage(Rectagnle.I_ObjectAddress, c_BroadCast, SCHM_BeginModify, c_NoEventData);
     Location := Rectagnle.Location;
     Location.x := -(SymbolWidth Div 2000000 * 2000000)/2;
     Location.y := Rectagnle.Location.y;
     Rectagnle.SetState_Location(Location);

     Location := Rectagnle.Corner;
     Location.x := SymbolWidth - (SymbolWidth Div 2000000 * 2000000)/2;
     Rectagnle.SetState_Corner(Location);

     For i := 0 to PinCount - 1 Do
     Begin
          If (PinArray[i].Orientation = 0)
             and (PinArray[i].OwnerPartId = Rectagnle.OwnerPartId) Then
          Begin
               Location := PinArray[i].Location;
               Location.x := Rectagnle.Corner.x;
               PinArray[i].SetState_Location(Location);
          End;
          If (PinArray[i].Orientation = 2)
             and (PinArray[i].OwnerPartId = Rectagnle.OwnerPartId) Then
          Begin
               Location := PinArray[i].Location;
               Location.x := Rectagnle.Location.x;
               PinArray[i].SetState_Location(Location);
          End;
     End;
     SchServer.RobotManager.SendMessage(Rectagnle.I_ObjectAddress, c_BroadCast, SCHM_EndModify  , c_NoEventData);
     CurrentLib.GraphicallyInvalidate;
End;

Procedure CheckSCHLib;
Var
   LibComp      :    ISCH_Component;
   Pins         :    Array[0..4000] of ISch_Pin;
   SCHRect      :    ISCH_Rectangle;
   Pin          :    ISCH_Pin;
   LibIterator  :    ISCH_Iterator;
   PinIterator  :    ISCH_Iterator;
   RectIterator :    ISCH_Iterator;
   Width        :    Integer;
   j            :    Integer;

Begin
     LibIterator := CurrentLib.SchLibIterator_Create;
     LibIterator.AddFilter_ObjectSet(MkSet(eSchComponent));
     LibComp := LibIterator.FirstSchObject;
     If LibComp <> Nil Then
     Begin
          If LibComp.Designator.Text <> 'U?' Then Exit;
          PinIterator := CurrentLib.SchLibIterator_Create;
          RectIterator := CurrentLib.SchLibIterator_Create;
          PinIterator.AddFilter_ObjectSet(MkSet(ePin));
          RectIterator.AddFilter_ObjectSet(MkSet(eRectangle));

          SCHRect := RectIterator. FirstSchObject;
          If SCHRect = Nil Then Exit;

          Pin := PinIterator.FirstSchObject;
          j := 0;
          PinCount := 0;
          While Pin <> Nil Do
          Begin
               Pins[j] := Pin;
               j := j + 1;
               PinCount := PinCount + 1;
               Pin := PinIterator.NextSchObject;
          End;

          While SCHRect <> Nil Do
          Begin
               Width : = SCHRect.Corner.x - SCHRect.Location.x;
               CalWidth(Pins, SCHRect);
               If (Width < (MaxCount*800000 + 3000000)) or (Width < 12000000) Then
               Begin
                    WideSymbol(Pins, SCHRect);
                    SymbolList.Add(LibComp.SymbolReference);
               End;
               SCHRect := RectIterator.NextSchObject;
          End;



          CurrentLib.SchIterator_Destroy(PinIterator);
          CurrentLib.SchIterator_Destroy(RectIterator);
     End;

     CurrentLib.SchIterator_Destroy(LibIterator);
End;

Procedure GetSCHLibDocuments;
Var
   i      :                  Integer;
Begin
     For i := 0 to project.DM_LogicalDocumentCount - 1 Do
     Begin
          Document := project.DM_LogicalDocuments(i);
          If Document.DM_DocumentKind = 'SCHLIB' Then
          Begin
               CurrentLib := Client.OpenDocument('SCHLIB', Document.DM_FullPath);
               If CurrentLib <> Nil Then
               Begin
                    Client.ShowDocument(CurrentLib);
                    CurrentLib := SCHServer.GetCurrentSchDocument;
                    If CurrentLib = Nil Then Eixt;
                    CheckSCHLib;
               End;
          End;
     End;
End;

Procedure GetPCBPorjects;
Begin
     WorkSpace := GetWorkSpace;
     If WorkSpace = Nil Then Exit;
     project := WorkSpace.DM_FreeDocumentsProject;
     GetSCHLibDocuments;
End;

Procedure ReviewAllOpenedLibs;
Begin
     SymbolList := TStringList.Create;
     GetPCBPorjects;
     ChangeReport;
     SymbolList.Free;
End;

Procedure ReivewCurrentLib;
Begin
     SymbolList := TStringList.Create;
     WorkSpace := GetWorkSpace;
     CurrentLib := SCHServer.GetCurrentSchDocument;
     CheckSCHLib;
     ChangeReport;
     SymbolList.Free;
End;
