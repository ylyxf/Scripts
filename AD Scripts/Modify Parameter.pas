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

//create a parameter list (a table), separate each parameter by 'tab'
Procedure getParameter;
Begin
     ParamIterator := LibComp.SchIterator_Create;
     ParamIterator.AddFilter_ObjectSet(Mkset(eParameter));

     Parameter := ParamIterator.FirstSchObject;       // creat a Iterator, then point to the first parameter
     While Parameter <> Nil Do
     Begin
          If Parameter.Name = 'PartNumber' Then       //modify parameter PartNUmber
          Begin
               Parameter.Text := LibComp.LibReference;
          End;

          Parameter := ParamIterator.NextSchObject;
     End;

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

     GetSCHLib;                          // get sch library file in current project and get parameters
End;
