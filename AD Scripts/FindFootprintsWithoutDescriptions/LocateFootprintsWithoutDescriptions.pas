Var
    CurrentLib            :   IPCB_Library;
    ComponentName         :   WideString;
    Document              :   IDocument;
    Project               :   IProject;
    WorkSpace             :   IWorkSpace;
    I, J, K, P            :   Integer;
    FileName              :   TDynamicString;
    LibraryIterator       :   IPCB_LibraryIterator;
    ComponentCount        :   Integer;
    LibComp               :   IPCB_LibComponent;
    S                     :   TDynamicString;
    ReportInfo            :   TStringList;
    SimpleInfo            :   TStringList;
    ReportDocument        :   IServerDocument;
    SimpleDocument        :   IServerDocument;
    ReportFilename        :   TDynamicString;
    SimpleRptFilename     :   TDynamicString;
    Yr,Mo,Dy,Hr,Mn,Sc,Ms  :   Integer;


Function GetPCBLibraryName() : WideString;
Var
    ModifiedLibName : WideString;
Begin
    ModifiedLibName := ExtractFileName(CurrentLib.Board.Filename);
    P := Pos('.PcbLib', ModifiedLibName);
    Delete(ModifiedLibName, P, 7);
    Result := ModifiedLibName;
End;

Procedure ProcessPCBComponents;
Begin
    LibraryIterator := CurrentLib.LibraryIterator_Create;
    LibraryIterator.SetState_FilterAll;
    ComponentCount := 0;
    Try
        LibComp := LibraryIterator.FirstPCBObject;
        While LibComp <> Nil Do
        Begin
            ComponentCount := ComponentCount + 1;
            ReportInfo.Add('| Footprint:     ' + LibComp.Name);
            ReportInfo.Add('| Footprint Description:     ' + LibComp.Description);

            If LibComp.Description = '' Then
            Begin
                 ReportInfo.Add('|');
                 ReportInfo.Add('|*********FOOTPRINT DOES NOT INCLUDE DESCRIPTION**********');
                 ReportInfo.Add('|');
            End;

            SimpleInfo.Add('| Footprint:     ' + LibComp.Name);
            LibComp := LibraryIterator.NextPCBObject;
        End;
     Finally

    End;
    CurrentLib.LibraryIterator_Destroy(LibraryIterator);
End;

//this procedure will fetch the library documents in the currently focused project
Procedure GetPCBLibraryDocuments;
Begin
    Project.DM_Compile;
    //loop through the documents in the project:

    For J := 0 to Project.DM_LogicalDocumentCount - 1 Do
    Begin
        Document := Project.DM_LogicalDocuments(J);
        //Check that the current document is a schematic:
        If Document.DM_DocumentKind = 'PCBLIB' Then
           Begin
           //open the schematic library:
           CurrentLib := Client.OpenDocument('PCBLIB', Document.DM_FullPath);

           If CurrentLib <> Nil Then
           Begin
               //make this pcblib the current document:
               Client.ShowDocument(CurrentLib);
               //now start treating it as a schematic, rather than a generic Altium document:
               CurrentLib := PCBServer.GetCurrentPCBLibrary;
               If CurrentLib = Nil Then Exit;

               // ShowMessage(CurrentLib.Board.Filename); //***DEBUG***//

               If CurrentLib.ComponentCount <> Nil Then
               Begin
                  ReportInfo.Add('|-------------------------------------------------------------');
                  ReportInfo.Add('| Library name:     ' + ExtractFileName(CurrentLib.Board.Filename));
                  ReportInfo.Add('| Library path:     ' + CurrentLib.Board.Filename);
                  ReportInfo.Add('|');

                  SimpleInfo.Add('-------------------------------------------------------------');
                  SimpleInfo.Add('| Library name:     ' + ExtractFileName(CurrentLib.Board.Filename));
                  SimpleInfo.Add('| Library path:     ' + CurrentLib.Board.Filename);
                  SimpleInfo.Add('|');

                  //process the library component information
                  ProcessPCBComponents;

                  ReportInfo.Add('|');
                  ReportInfo.Add('|-------------------------------------------------------------');

                  SimpleInfo.Add('|');
                  SimpleInfo.Add('|-------------------------------------------------------------');
               End
               Else
                  //should never, ever get here.  if it does, something went horribly wrong
               Begin
                  ReportInfo.Add('|-------------------------------------------------------------');
                  ReportInfo.Add('| Library name:     ' + ExtractFileName(CurrentLib.Board.Filename));
                  ReportInfo.Add('| Library path:     ' + CurrentLib.Board.Filename);
                  ReportInfo.Add('|');
                  ReportInfo.Add('|***************Library contains no components****************');
                  ReportInfo.Add('|');
                  ReportInfo.Add('|-------------------------------------------------------------');
               End;

               //ShowMessage(CurrentLib.DocumentName); //***DEBUG***//
           End;
        End;
    End;
End;

//this is the entry point and will iterate across all of the projects currently in the Workspace
Procedure GetPCBProjects;
Begin
    WorkSpace := GetWorkSpace;
    If WorkSpace = Nil Then Exit;

    // Create a TStringList object to store data
    ReportInfo := TStringList.Create;

    // Create a TStringList object to store data
    SimpleInfo := TStringList.Create;
    SimpleInfo.Clear;

    For I := 0 To WorkSpace.DM_ProjectCount - 1 Do
    Begin
        Project := WorkSpace.DM_Projects(I);
        If (Project.DM_ObjectKindString = 'PCB Project') then
        GetPCBLibraryDocuments;
    End;

    //generate a unique filename
    DecodeDate(Date,Yr,Mo,Dy);
    DecodeTime(Time,Hr,Mn,Sc,Ms);
    ReportFilename := ('G:\PCB Footprint Description Report (' + IntToStr(Yr) + '-' + IntToStr(Mo) + '-'
                  + IntToStr(Dy) + '_' + IntToStr(Hr) + '-' + IntToStr(Mn) + '-' + IntToStr(Sc) + ').txt');

    SimpleRptFilename := ('G:\(Simple) PCB Library Naming Report (' + IntToStr(Yr) + '-' + IntToStr(Mo) + '-'
                  + IntToStr(Dy) + '_' + IntToStr(Hr) + '-' + IntToStr(Mn) + '-' + IntToStr(Sc) + ').txt');

    //generate and open the simple report file
    SimpleInfo.SaveToFile(SimpleRptFilename);
    SimpleDocument := Client.OpenDocument('Text', SimpleRptFilename);
    SimpleDocument.Modified := True;
    If SimpleDocument <> Nil Then
        Client.ShowDocument(SimpleDocument);

    //generate and open the detailed report file
    ReportInfo.SaveToFile(ReportFilename);
    ReportDocument := Client.OpenDocument('Text', ReportFilename);
    ReportDocument.Modified := True;
    If ReportDocument <> Nil Then
        Client.ShowDocument(ReportDocument);

    ReportInfo.Free;
    SimpleInfo.Free;

End;

Procedure StartHere;
Begin
     GetPCBProjects();
End;
