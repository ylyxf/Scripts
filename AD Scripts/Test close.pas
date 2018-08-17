Var
   i : Integer;
   Document : IDocument ;
   Project : IProject;
   CurrentLib   :   ISCH_Lib;
   Workspace    :   IWorkSpace;


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
                 //CurrentLib := SCHServer.GetCurrentSchDocument;                         // treat the general document as a Sch lib document
                 //ShowMessage(CurrentLib.Handle);
                 //SCHServer.DestroySchLibrary(CurrentLib);
                 //Client.HideDocument(CurrentLib);
                 Client.CloseDocument(Document);
                 //Client.CloseDocument(CurrentLib);
           End;
      End;
End;
