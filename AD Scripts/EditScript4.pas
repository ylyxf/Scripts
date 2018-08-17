
Var
   Project  :   IProject;
   Workspace :    IWorkspace;
   i, SlashP, ComP         :    Integer;
   Document  :    IDocument;
   CurrentLib     :         IPCB_Library;
   LibraryIterator          :            IPCB_LibraryIterator;
   LibComp                  :            IPCB_LibComponent;
   ImportDesc               :            TStringList;
   ImportLibName            :            TStringList;
   TrimedDesc               :            WideString;


Procedure GetDesc;
Begin
     LibraryIterator := CurrentLib.LibraryIterator_Create;
     LibraryIterator.SetState_FilterAll;
     LibComp := LibraryIterator.FirstPCBObject;

     While LibComp <> Nil Do
     Begin
          ShowMessage(LibComp.Description);
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

procedure TForm1.Button1Click(Sender: TObject);
begin
     If TMemo1.Text = '' Then
        Begin
        ShowMessage('Please input description');
        End
     Else
         Begin
         ImportDesc := TStringList.Create;
         ImportLibName := TStringList.Create;
         SlashP := Pos('|' , TMemo1.Text);
         While SlashP > 1 do
         Begin
         TrimedDesc := Copy(TMemo1.Text , 1, SlashP-1);
         ComP := Pos(':' , TrimedDesc);
         ImportDesc.Add(Copy(TrimedDesc, comP + 1, Length(TrimedDesc)-comP+1));
         ImportLibName.Add(Copy(TrimedDesc, 1, comP -1));
         TMemo1.Text := Copy(TMemo1.Text, SlashP + 1, Length(TMemo1.Text) - SlashP + 1);
         End;





         GetPCBLibraryDoc;
         ImportDesc.Free;
         End;
end;

procedure TForm1.Form1Create(Sender: TObject);
begin
TMemo1.Text := '';
end;

Var
st, st1 : WideString;
ps : Integer;
Procedure testString;
Begin
st := 'KSDC012551:SD Card socket|S1206RGBSDJC:SM RGB LED; 4-Leads; Body 3.2 x 1.5 mm (1206-size)';
ps := Pos('|' , st);
st1 :=  Copy(st, ps + 1, Length(st) - ps + 1);
showMessage(st1);
End;

