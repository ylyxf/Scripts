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
   PadLength                          :   Single;
   Pad                                :   IPCB_PAD;
   Gap                                :   Single;
   PadRotation                        :   Single;

Procedure GetPadsInfo;
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
          PadRotation := Pad.Rotation;
          If (PadRotation = 0) or (PadRotation = 180) Then
             Begin
                  PadLength := CoordToMMs(Pad.TopXsize);
             End
          Else PadLength := CoordToMMs(Pad.TopYsize);

           ReportInfo.Add(Libcomp.Name + '^' + FloattoStr(PadLength) + '^' + FloattoStr(LocationX1) + '^' + FloattoStr(LocationY1));

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
            GetPadsInfo;

       End;

  End;
End ;



Procedure Start;
Begin
      ReportInfo := TStringList.Create;
      GetPCBLibraryDoc;
      DecodeDate(Date,Yr,Mo,Dy);
      DecodeTime(Time,Hr,Mn,Sc,Ms);      //get current date
     ReportFilename := ('G:\Chip Pads Overview (' + IntToStr(Yr) + '-' + IntToStr(Mo) + '-'
                  + IntToStr(Dy) + '_' + IntToStr(Hr) + '-' + IntToStr(Mn) + '-' + IntToStr(Sc) + ').txt');  //use current date to generate a unique report file name
     ReportInfo.SaveToFile(ReportFilename);     //save report to file
     ReportDocument := Client.OpenDocument('Text', ReportFilename);
     If ReportDocument <> Nil Then
        Client.ShowDocument(ReportDocument);

    ReportInfo.Free;
End;
