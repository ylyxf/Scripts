Var
   CurrentLib   :   ISCH_Lib;
   Document     :   IDocument;
   Workspace    :   IWorkSpace;
   Project      :   IProject;
   i            :   Integer;
   ParamCounts   :   Integer;
   LibraryIterator  :       Isch_Iterator;
   ParamIterator    :       Isch_Iterator;
   LibComp          :       ISch_Component;
   Parameter        :       ISch_Parameter;
   Yr,Mo,Dy,Hr,Mn,Sc,Ms  :   Integer;
   ReportFilename        :   TDynamicString;
   ReportInfo            :   TStringList;
   ReportStr, ParamsStr   :   WideString;
   ReportDocument        :   IServerDocument;
   ModelsIterator             :   Isch_Iterator;
   PCBModels  : ISch_Implementation;

//create a parameter list (a table), separate each parameter by 'tab'
Procedure getParameter;
Begin
     ParamIterator := LibComp.SchIterator_Create;
     ParamIterator.AddFilter_ObjectSet(Mkset(eParameter));

     Parameter := ParamIterator.FirstSchObject;       // creat a Iterator, then point to the first parameter
     ParamCounts := 0;
     ReportStr := LibComp.OwnerDocument.DocumentName + '^';      //add library file name
     ReportStr := ReportStr + LibComp.LibReference + '^';          // a sting = Library reference name  + 'tab'
     ReportStr := reportstr + Libcomp.ComponentDescription + '^';  // add component description
     ReportStr := ReportStr + Libcomp.Designator.Text + '^';  // add designator

     ModelsIterator := LibComp.SchIterator_Create;    // get PCB footprint name of this component and add to report
     ModelsIterator.AddFilter_ObjectSet(Mkset(eImplementation));
     PCBModels :=  ModelsIterator.FirstSchObject;
     While PCBModels <> Nil Do
     Begin
           If PCBModels.ModelType = 'PCBLIB' Then
           Begin
                ReportStr := ReportStr + PCBModels.ModelName + '^';
           End;
           PCBModels := ModelsIterator.NextSchObject;
     End;

    // ReportStr := ReportStr + LibComp
     ParamsStr := '';
     While Parameter <> Nil Do
     Begin
          If (Parameter.IsSystemParameter = False && (Parameter.Name <> 'Comment')) Then      // component comment is also a part of parameter, so it should be skipped
          Begin
          ParamsStr := ParamsStr + Parameter.Name + ':' + Parameter.Text + '^';               // previous parameter name + value + current parameter name + value
          ParamCounts := ParamCounts + 1;
          End;
          Parameter := ParamIterator.NextSchObject;
     End;
     If ParamCounts <> 0 Then
     ReportStr := ReportStr + ParamsStr;
     ReportInfo.Add(ReportStr);             // symbol name + parameter name + vaule as a row in talbe
End;


// loop through a schlib file to get library components
Procedure ProcessPerComp;
Begin
     LibraryIterator := CurrentLib.SchLibIterator_Create;       //creata a Schlib Iterator
     LibraryIterator.AddFilter_ObjectSet(Mkset(eSchComponent));  // set the Iterator filter object, the object list can be found in Altium Wiki, Schematic API Types -> TObjectId
     If  LibraryIterator = Nil Then Exit;

     LibComp :=  LibraryIterator.FirstSchObject;                // point to the first sch library component
     While LibComp <> Nil Do
     Begin
          getParameter;
          LibComp := LibraryIterator.NextSchObject;             // move to next sch library component
     End;
     CurrentLib.SchIterator_Destroy(LibraryIterator);          // destroy iterator, free memory
End;

Procedure GetSCHLib;
Begin
      WorkSpace := GetWorkspace;                        // get current work space
      Project := WorkSpace.DM_FocusedProject;           // get cureeent project
      For i := 0 to Project.DM_LogicalDocumentCount -1 Do    //loop through  files in current project
      Begin
           Document := Project.DM_LogicalDocuments(i);    // get a schlib file as general document
           If Document.DM_DocumentKind = 'SCHLIB' Then
           Begin
                 CurrentLib := Client.OpenDocument('SCHLIB' , Document.DM_FullPath);    //open schlib file
                 Client.ShowDocumentDontFocus(CurrentLib);                              // make the opened file as current document
                 CurrentLib := SCHServer.GetCurrentSchDocument;                         // treat the general document as a Sch lib document
                 ProcessPerComp;
           End;
      End;
End;

// script start from here, get library file and export paramter list
Procedure Start;
Begin
     ReportInfo := TStringList.Create;   //preapare string list for result output
     GetSCHLib;                          // get sch library file in current project and get parameters
     DecodeDate(Date,Yr,Mo,Dy);
     DecodeTime(Time,Hr,Mn,Sc,Ms);      //get current date
     ReportFilename := ('G:\SCH Library Parameter Report (' + IntToStr(Yr) + '-' + IntToStr(Mo) + '-'
                  + IntToStr(Dy) + '_' + IntToStr(Hr) + '-' + IntToStr(Mn) + '-' + IntToStr(Sc) + ').txt');  //use current date to generate a unique report file name
     ReportInfo.SaveToFile(ReportFilename);     //save report to file
     ReportDocument := Client.OpenDocument('Text', ReportFilename);
     If ReportDocument <> Nil Then
        Client.ShowDocument(ReportDocument);

    ReportInfo.Free;
End;
