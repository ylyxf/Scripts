Var
    CurrentLib            :   ISCH_Lib;
    ComponentName         :   WideString;
    Document              :   IDocument;
    Project               :   IProject;
    WorkSpace             :   IWorkSpace;
    I, J, K, L, P         :   Integer;
    FileName              :   TDynamicString;
    LibraryIterator       :   ISch_Iterator;
    ComponentCount        :   Integer;
    LibComp               :   ISch_Component;
    S                     :   TDynamicString;
    PIterator             :   ISch_Iterator;
    Parameter             :   ISch_Parameter;
    ImplIterator          :   ISch_Iterator;
    SchImplementation     :   ISch_Implementation;
    ReportInfo            :   TStringList;
    SimpleInfo            :   TStringList;
    DuplicatesList        :   TStringList;
    GenericList           :   TStringList;
    DuplicateLoc          :   Integer;
    ReportDocument        :   IServerDocument;
    SimpleDocument        :   IServerDocument;
    ReportFilename        :   TDynamicString;
    SimpleRptFilename     :   TDynamicString;
    Yr,Mo,Dy,Hr,Mn,Sc,Ms  :   Integer;
    genericTest           :   Boolean;

Function ProcessGenerics() : Boolean;
Begin
    // test if this component is a diode
    If ((Pos('DIOD',LibComp.LibReference) <> 0) || (Pos('Diod',LibComp.LibReference) <> 0)
       || (Pos('diod',LibComp.LibReference) <> 0))  Then
    Begin
       genericTest := True;
    End;

    // test if this component is a mosfet
    If ((Pos('MOS',LibComp.LibReference) <> 0) || (Pos('Mos',LibComp.LibReference) <> 0)
       || (Pos('mos',LibComp.LibReference) <> 0))  Then
    Begin
       genericTest := True;
    End;

    // test if this component is a FET
    If ((Pos('FET',LibComp.LibReference) <> 0) || (Pos('Fet',LibComp.LibReference) <> 0)
       || (Pos('fet',LibComp.LibReference) <> 0))  Then
    Begin
       genericTest := True;
    End;

    // test if this component is a PNP
    If ((Pos('PNP',LibComp.LibReference) <> 0) || (Pos('Pnp',LibComp.LibReference) <> 0)
       || (Pos('pnp',LibComp.LibReference) <> 0))  Then
    Begin
       genericTest := True;
    End;

    // test if this component is a NPN
    If ((Pos('NPN',LibComp.LibReference) <> 0) || (Pos('Npn',LibComp.LibReference) <> 0)
       || (Pos('npn',LibComp.LibReference) <> 0))  Then
    Begin
       genericTest := True;
    End;

    // test if this component is a XTAL
    If ((Pos('XTAL',LibComp.LibReference) <> 0) || (Pos('Xtal',LibComp.LibReference) <> 0)
       || (Pos('xtal',LibComp.LibReference) <> 0))  Then
    Begin
       genericTest := True;
    End;

    // test if this component is a connector
    If ((Pos('CON',LibComp.LibReference) <> 0) || (Pos('Con',LibComp.LibReference) <> 0)
       || (Pos('con',LibComp.LibReference) <> 0))  Then
    Begin
       genericTest := True;
    End;

    Result := genericTest;
End;

//this function parses the filename to return just the base-name without the extension
Function GetLibraryName() : WideString;
Var
    ModifiedLibName : WideString;
Begin
    ModifiedLibName := ExtractFileName(CurrentLib.DocumentName);
    P := Pos('.SCHLIB', UpperCase(ModifiedLibName));
    Delete(ModifiedLibName, P, 7);
    Result := ModifiedLibName;
End;

Procedure ProcessParameters;
Begin
    Try
        L := 0;
        // reset the component comment and description
        LibComp.Comment.Text := '*';
        LibComp.ComponentDescription := '';
        ReportInfo.Add('|');
        ReportInfo.Add('| Completed: Component comment and description reset successfully!');

        // make a list of user parameters and delete
        ReportInfo.Add('|');
        ReportInfo.Add('| User parameters for this symbol: ');

        PIterator := LibComp.SchIterator_Create;
        PIterator.AddFilter_ObjectSet(MkSet(eParameter));

        Parameter := PIterator.FirstSchObject;
        While Parameter <> Nil Do
        Begin
            If (Parameter.IsSystemParameter = False && (Parameter.Name <> 'Comment')) Then
            Begin
               ReportInfo.Add('| ' + Parameter.Name + ' : ' + Parameter.CalculatedValueString);
               LibComp.RemoveSchObject(Parameter);
               L := L + 1;
            End;
            Parameter := PIterator.NextSchObject;
        End;
    Finally
        If L = 0 Then ReportInfo.Add('| ...none');
        LibComp.SchIterator_Destroy(PIterator);
        ReportInfo.Add('|');
        ReportInfo.Add('| Completed:  All user parameters deleted successfully!');
    End;
End;

Procedure ProcessModels;
Begin
    ImplIterator := LibComp.SchIterator_Create;
    ImplIterator.AddFilter_ObjectSet(MkSet(eImplementation));

    Try
        SchImplementation := ImplIterator.FirstSchObject;
        While SchImplementation <> Nil Do
        Begin
            ReportInfo.Add('|');
            ReportInfo.Add(' | Implementation Model details:');
            ReportInfo.Add(' | ModelName: '   + SchImplementation.ModelName +
                           ' ModelType: '   + SchImplementation.ModelType +
                           ' Description: ' + SchImplementation.Description);

            //alert robots that component is about to be modified
            SchServer.ProcessControl.PreProcess(CurrentLib, '');
            SchServer.RobotManager.SendMessage(LibComp.I_ObjectAddress, c_BroadCast, SCHM_BeginModify, c_NoEventData);

            //delete the model from the component
            LibComp.RemoveSchImplementation(SchImplementation);
            SchImplementation.DeleteAll;

            //alert the robots that changes are complete
            CurrentLib.GraphicallyInvalidate;
            SchServer.RobotManager.SendMessage(LibComp.I_ObjectAddress, c_BroadCast, SCHM_EndModify  , c_NoEventData);

            CurrentLib.GraphicallyInvalidate();
            SchImplementation := ImplIterator.NextSchObject;
        End;
    Finally
        LibComp.SchIterator_Destroy(ImplIterator);
        ReportInfo.Add('|');
        ReportInfo.Add('| Completed:  All component models removed successully!');
    End;
End;

//this procedure will iterate across components and rename them, also generate a report
Procedure ProcessComponents;
Begin
    // get the library object for the library iterator.
    LibraryIterator := CurrentLib.SchLibIterator_Create;
    LibraryIterator.AddFilter_ObjectSet(MkSet(eSchComponent));
    If LibraryIterator = Nil Then Exit;

    ComponentCount := 0;

    Try
        // iterate across components in the current library and make a list
        LibComp := LibraryIterator.FirstSchObject;
        While LibComp <> Nil Do
        Begin
            genericTest := False;
            ComponentCount := ComponentCount + 1;
            ReportInfo.Add('| Component:     ' + LibComp.LibReference);
            SimpleInfo.Add('| Component:     ' + LibComp.LibReference);

            //genericTest := ProcessGenerics();
            If genericTest Then
            Begin
                 GenericList.Add(LibComp.LibReference);
                 GenericList.Add(CurrentLib.DocumentName);
            End;

            If (DuplicatesList.IndexOf(LibComp.LibReference) <> -1) Then
            Begin
                DuplicatesList.Add('------------ERROR:  Duplicate Object Name "' + LibComp.LibReference + '"------------');
                DuplicatesList.Add('>> ' + CurrentLib.DocumentName);
            End;
            DuplicatesList.Add(LibComp.LibReference);

            LibComp := LibraryIterator.NextSchObject;

        End;
    Finally
        If ComponentCount <> 1 then
        Begin
            //ShowMessage('There are ' + IntToStr(ComponentCount) + ' components in this library');   //***DEBUG***//
            ReportInfo.Add('|');
            ReportInfo.Add('| ************ERROR: Library contains ' + IntToStr(ComponentCount) + ' components************');
        End;
        // we are finished fetching symbols of the current library.
    End;

    LibComp := LibraryIterator.FirstSchObject;
    S := GetLibraryName();

    //Delete any user parameters and reset comment and description
    ProcessParameters();

    //Delete any models added to this component
    ProcessModels();

    //If ((ComponentCount = 1) && (LibComp.LibReference <> S) && (GenericTest <> True))  Then
    If ((ComponentCount = 1) && (LibComp.LibReference <> S))  Then  //null the genericTest
    Begin
       Try
          // Prepare the Sch software agents for changes.
          SchServer.ProcessControl.PreProcess(CurrentLib, '');
          SchServer.RobotManager.SendMessage(LibComp.I_ObjectAddress, c_BroadCast, SCHM_BeginModify, c_NoEventData);
          LibComp.LibReference := S;

          CurrentLib.GraphicallyInvalidate;
          SchServer.RobotManager.SendMessage(LibComp.I_ObjectAddress, c_BroadCast, SCHM_EndModify  , c_NoEventData);
       Finally
          // Clean up the robots in Schematic editor
          SchServer.ProcessControl.PostProcess(CurrentLib, '');
          ReportInfo.Add('| Component renamed:     ' + LibComp.LibReference);
          ReportInfo.Add('|');

          If (DuplicatesList.IndexOf(LibComp.LibReference) <> -1) Then
          Begin
              DuplicatesList.Add('------------ERROR:  Duplicate Object Name "' + LibComp.LibReference + '"------------');
              DuplicatesList.Add('>> ' + CurrentLib.DocumentName);
          End;
          DuplicatesList.Add('»' + LibComp.LibReference);

       End;
    End;

    If (GenericTest = True) Then
    Begin
          ReportInfo.Add('| ************ ERROR: Possible Generic - DID NOT RENAME ************');
          ReportInfo.Add('|');
    End;
    CurrentLib.SchIterator_Destroy(LibraryIterator);
End;

//this procedure will fetch the library documents in the currently focused project
Procedure GetLibraryDocuments;
Begin
    Project.DM_Compile;
    //loop through the documents in the project:

    For J := 0 to Project.DM_LogicalDocumentCount - 1 Do
    Begin
        Document := Project.DM_LogicalDocuments(J);
        //Check that the current document is a schematic:
        If Document.DM_DocumentKind = 'SCHLIB' Then
           Begin
           //open the schematic library:
           CurrentLib := Client.OpenDocument('SCHLIB', Document.DM_FullPath);
           //check that the schematic could be opened:
           If CurrentLib <> Nil Then
           Begin
               //make this schematic the current document:
               Client.ShowDocument(CurrentLib);
               //now start treating it as a schematic, rather than a generic Altium document:
               CurrentLib := SchServer.GetCurrentSchDocument;
               If CurrentLib = Nil Then Exit;

               If CurrentLib.LibIsEmpty <> True Then
               Begin
                  ReportInfo.Add('-------------------------------------------------------------');
                  ReportInfo.Add('| Library name:     ' + ExtractFileName(CurrentLib.DocumentName));
                  ReportInfo.Add('| Library path:     ' + CurrentLib.DocumentName);
                  ReportInfo.Add('|');

                  SimpleInfo.Add('-------------------------------------------------------------');
                  SimpleInfo.Add('| Library name:     ' + ExtractFileName(CurrentLib.DocumentName));
                  SimpleInfo.Add('| Library path:     ' + CurrentLib.DocumentName);
                  SimpleInfo.Add('|');

                  //process the library component information
                  ProcessComponents;

                  ReportInfo.Add('|');
                  ReportInfo.Add('-------------------------------------------------------------');

                  SimpleInfo.Add('|');
                  SimpleInfo.Add('-------------------------------------------------------------');
               End
               Else
                  //should never, ever get here.  if it does, something went horribly wrong
               Begin
                  ReportInfo.Add('-------------------------------------------------------------');
                  ReportInfo.Add('| Library name:     ' + ExtractFileName(CurrentLib.DocumentName));
                  ReportInfo.Add('| Library path:     ' + CurrentLib.DocumentName);
                  ReportInfo.Add('|');
                  ReportInfo.Add('|**************Library contains no components****************');
                  ReportInfo.Add('|');
                  ReportInfo.Add('-------------------------------------------------------------');
               End;

               //ShowMessage(CurrentLib.DocumentName); //***DEBUG***//
           End;
        End;
    End;
End;

//this is the entry point and will iterate across all of the projects currently in the Workspace
Procedure GetProjects;
Begin
    WorkSpace := GetWorkSpace;
    If WorkSpace = Nil Then Exit;

    // Create a TStringList object to store data
    ReportInfo := TStringList.Create;
    ReportInfo.Clear;

    // Create a TStringList object to store data
    SimpleInfo := TStringList.Create;
    SimpleInfo.Clear;

    // Create a TStringList object to store data
    GenericList := TStringList.Create;
    GenericList.Clear;
    GenericList.Add(#13 + #13 + '-------------------------------------------------------------');
    GenericList.Add(#13 + 'Generics List: (Searching for possible generic symbols)');

    // Create a TStringList object to store data
    DuplicatesList := TStringList.Create;
    DuplicatesList.Clear;
    DuplicatesList.Add(#13 + #13 + '-------------------------------------------------------------');
    DuplicatesList.Add(#13 + 'Component List: (Searching for duplicate components)');

    For I := 0 To WorkSpace.DM_ProjectCount - 1 Do
    Begin
        Project := WorkSpace.DM_Projects(I);
        If (Project.DM_ObjectKindString = 'PCB Project') then
        GetLibraryDocuments;
    End;

    //generate a unique filename
    DecodeDate(Date,Yr,Mo,Dy);
    DecodeTime(Time,Hr,Mn,Sc,Ms);
    ReportFilename := ('G:\SCH Library Renaming Report (' + IntToStr(Yr) + '-' + IntToStr(Mo) + '-'
                  + IntToStr(Dy) + '_' + IntToStr(Hr) + '-' + IntToStr(Mn) + '-' + IntToStr(Sc) + ').txt');

    SimpleRptFilename := ('G:\(Simple) SCH Library Naming Report (' + IntToStr(Yr) + '-' + IntToStr(Mo) + '-'
                  + IntToStr(Dy) + '_' + IntToStr(Hr) + '-' + IntToStr(Mn) + '-' + IntToStr(Sc) + ').txt');

    //generate and open the simple report file
    SimpleInfo.SaveToFile(SimpleRptFilename);
    SimpleDocument := Client.OpenDocument('Text', SimpleRptFilename);
    SimpleDocument.Modified := True;
    If SimpleDocument <> Nil Then
        Client.ShowDocument(SimpleDocument);

    //add the list of duplicates to the end of the report file
    ReportInfo.Add(DuplicatesList.Text);

    //add the list of possible generics to the report file
    ReportInfo.Add(GenericList.Text);

    //generate and open the detailed report file
    ReportInfo.SaveToFile(ReportFilename);
    ReportDocument := Client.OpenDocument('Text', ReportFilename);
    ReportDocument.Modified := True;
    If ReportDocument <> Nil Then
        Client.ShowDocument(ReportDocument);

    ReportInfo.Free;
    SimpleInfo.Free;
    DuplicatesList.Free;
    GenericList.Free;

End;

Procedure StartHere;
Begin
     //ProcessGenerics;
     GetProjects();
End;

