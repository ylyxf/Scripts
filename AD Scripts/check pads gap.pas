Var
   Project                  :   IProject;
   Workspace                :   IWorkspace;
   i                        :   Integer;
   Document                 :   IDocument;
   CurrentLib               :   IPCB_Library;
   LibraryIterator          :   IPCB_LibraryIterator;
   PadIterator              :   IPCB_GroupIterator;
   LibComp                  :   IPCB_LibComponent;
   ReportFilename           :   TDynamicString;
   ReportInfo               :   TStringList;
   ReportStr, ParamsStr     :   WideString;
   ReportDocument           :   IServerDocument;
   Yr,Mo,Dy,Hr,Mn,Sc,Ms     :   Integer;
   LocationX1, LocationX2             :   Single;
   LocationY1, LocationY2             :   Single;
   PadWidth                           :   Single;
   Pad                                :   IPCB_PAD;
   Gap                                :   Single;

Procedure GetGap;
Begin
     LibraryIterator := CurrentLib.LibraryIterator_Create;
     LibraryIterator.AddFilter_ObjectSet(Mkset(eComponentObject));
     LibraryIterator.SetState_FilterAll;
     LibComp := LibraryIterator.FirstPCBObject;

     While LibComp <> Nil Do
     Begin
          PadIterator := LibComp.GroupIterator_Create;
          PadIterator.AddFilter_ObjectSet(mkset(ePadObject));
          Pad := PadIterator.FirstPCBObject;

          LocationX1 := CoordToMMs(Pad.x);
          LocationY1 := CoordToMMs(Pad.y);

          If (Pad.Rotation := 90) or (Pad.Rotation := 270) Then
             Begin
                  PadWidth := CoordToMMs(Pad.TopXsize);
             End
          Else PadWidth := CoordToMMs(Pad.TopYsize);

          Pad := PadIterator.NextPCBObject;
          LocationX2 := CoordToMMs(Pad.x);
          LocationY2 := CoordToMMs(Pad.y);

          Gap :=  abs(LocationX1-LocationX2) - PadWidth;
          If (Gap < 0.2) Then
          Begin
           ReportInfo.Add(Libcomp.Name + '^^' + FloattoStr(Gap));
          End;

          LibComp.GroupIterator_Destroy(PadIterator);
          LibComp := LibraryIterator.NextPCBObject;
     End;

     CurrentLib.LibraryIterator_Destroy(LibraryIterator);
End;

Procedure GetPCBLibraryDoc;
Begin

  Workspace := GetWorkSpace;
  Project :=   Workspace.DM_FocusedProject;
 // ShowMessage(Project.DM_ObjectKindString);

  For i := 0 to Project.DM_LogicalDocumentCount - 1 Do
  Begin
       Document := Project.DM_LogicalDocuments(i);

       If Document.DM_DocumentKind = 'PCBLIB' Then
       Begin
            CurrentLib := Client.OpenDocument('PCBLIB', Document.DM_FullPath);
            Client.ShowDocument(CurrentLib);
            CurrentLib := PCBServer.GetCurrentPCBLibrary;
            GetGap;

       End;

  End;
End ;



Procedure Start;
Begin
      ReportInfo := TStringList.Create;
      GetPCBLibraryDoc;
      DecodeDate(Date,Yr,Mo,Dy);
      DecodeTime(Time,Hr,Mn,Sc,Ms);      //get current date
     ReportFilename := ('G:\Pad Gap Report (' + IntToStr(Yr) + '-' + IntToStr(Mo) + '-'
                  + IntToStr(Dy) + '_' + IntToStr(Hr) + '-' + IntToStr(Mn) + '-' + IntToStr(Sc) + ').txt');  //use current date to generate a unique report file name
     ReportInfo.SaveToFile(ReportFilename);     //save report to file
     ReportDocument := Client.OpenDocument('Text', ReportFilename);
     If ReportDocument <> Nil Then
        Client.ShowDocument(ReportDocument);

    ReportInfo.Free;
End;
