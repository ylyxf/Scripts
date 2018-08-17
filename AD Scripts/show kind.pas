Var
   i : Integer;
   Document : IDocument ;
   Project : IProject;

Begin
     Project := GetWorkspace.DM_FocusedProject;
     If Project = Nil Then Exit;
     For i := 0 To Project.DM_LogicalDocumentCount - 1 Do
     Begin
          Document := Project.DM_LogicalDocuments(i);
          ShowMessage(Document.DM_DocumentKind);
     End;
End
