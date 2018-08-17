procedure TForm2.Button1Click(Sender: TObject);

var

FileName:String;
NameNo: interger;
IsExist: Boolean;
i: Integer;
Workspace:IWorkspace;
Document: IServerDocument;
DocumentKind : String;
begin

 FileName:= Nil;
 Client.StartServer('SCHlib');
 Client.SendMessage('WorkspaceManager:OpenObject','Kind=PcbProject | ObjectKind=NewAnything',1024,Nil);

 NameNo:= Memo1.Lines.Count;
 i:= 0;
 For i:= 0 to NameNo-1 do
     begin
          FileName:=Memo1.Lines[i];
          IsExist:= FileExists(FileName);
          If IsExist = True then
             begin
                 DocumentKind:= Client.GetDocumentKindFromDocumentFileName(FileName,false);
                  Document:=Client.OpenDocument(DocumentKind,FileName);

                   If Document <> Nil then
                      begin
                           Workspace:=GetWorkspace;
                           If Workspace <>Nil then
                              begin Workspace.DM_FocusedProject.DM_AddSourceDocument(Document.FileName);  End;

                           Client.ShowDocument(Document);

                      end;
             End;
     end;

end;



procedure TForm2.Form2Create(Sender: TObject);
begin
Memo1.ScrollBars:=ssBoth;
Button1.caption:='Open File';
end;

