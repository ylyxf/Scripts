Var
   Project  :   IProject;
   Workspace :    IWorkspace;
   i         :    Integer;
   Document  :    IDocument;
   CurrentLib     :         IPCB_Library;
   LibraryIterator          :            IPCB_LibraryIterator;
   LibComp                  :            IPCB_LibComponent;
   ReportFilename        :   TDynamicString;
   ReportInfo            :   TStringList;
   ReportStr, ParamsStr   :   WideString;
   ReportDocument        :   IServerDocument;
   Yr,Mo,Dy,Hr,Mn,Sc,Ms  :   Integer;

Procedure GetDesc;
Begin
     LibraryIterator := CurrentLib.LibraryIterator_Create;
     LibraryIterator.SetState_FilterAll;
     LibComp := LibraryIterator.FirstPCBObject;

     While LibComp <> Nil Do
     Begin
          ReportInfo.Add(Libcomp.Name + '^^' + LibComp.Description);
          //ShowMessage(LibComp.Description);
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
            GetDesc;

       End;

  End;
End ;



Procedure Start;
Begin
      ReportInfo := TStringList.Create;
      GetPCBLibraryDoc;
      DecodeDate(Date,Yr,Mo,Dy);
      DecodeTime(Time,Hr,Mn,Sc,Ms);      //get current date
     ReportFilename := ('G:\Footprint Description Report (' + IntToStr(Yr) + '-' + IntToStr(Mo) + '-'
                  + IntToStr(Dy) + '_' + IntToStr(Hr) + '-' + IntToStr(Mn) + '-' + IntToStr(Sc) + ').txt');  //use current date to generate a unique report file name
     ReportInfo.SaveToFile(ReportFilename);     //save report to file
     ReportDocument := Client.OpenDocument('Text', ReportFilename);
     If ReportDocument <> Nil Then
        Client.ShowDocument(ReportDocument);

    ReportInfo.Free;
End;
