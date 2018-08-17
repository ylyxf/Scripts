{

}

{..............................................................................}
Procedure ReportExistingProjectsInDXP;
Var
    WorkSpace             : IWorkSpace;
    Project               : IProject;
    Document              : IDocument;
    I                     : Integer;
    K                     : Integer;
    ReportFile            : Text;
    MSFileName            : TDynamicString;
    FileName              : TDynamicString;
    ReportDocument        : IServerDocument;
    ManagedSheetList      : TStringList;
    MSLDocument           : IDocument;
    MSPos, HNPos          : Integer;
    Yr,Mo,Dy,Hr,Mn,Sc,Ms  : Integer;

Begin
    WorkSpace := GetWorkSpace;
    If WorkSpace = Nil Then Exit;

    ManagedSheetList := TStringList.Create;

    //generate a unique filename
    DecodeDate(Date,Yr,Mo,Dy);
    DecodeTime(Time,Hr,Mn,Sc,Ms);

    Filename := ('G:\Project_Report (' + IntToStr(Yr) + '-' + IntToStr(Mo) + '-'
                  + IntToStr(Dy) + '_' + IntToStr(Hr) + '-' + IntToStr(Mn) + '-' + IntToStr(Sc) + ').txt');

    MSFileName := ('G:\MSheet_Report (' + IntToStr(Yr) + '-' + IntToStr(Mo) + '-'
                  + IntToStr(Dy) + '_' + IntToStr(Hr) + '-' + IntToStr(Mn) + '-' + IntToStr(Sc) + ').txt');

    AssignFile(ReportFile, FileName);
    Rewrite(ReportFile);

    For I := 0 To WorkSpace.DM_ProjectCount - 1 Do
    Begin
        Project := WorkSpace.DM_Projects(I);

        Writeln(ReportFile, 'Project : ', Project.DM_ProjectFileName);

        For K := 0 To Project.DM_LogicalDocumentCount - 1 Do
        Begin

            //get the documents that are SCHDOC files...
            Document := Project.DM_LogicalDocuments(K);
            If Pos('.SCHLIB', UpperCase(Document.DM_FullPath)) >= 1 then
            Begin
                 //ShowMessage(Document.DM_FullPath);
                 Writeln(ReportFile, Document.DM_FullPath);
            End;

           //get the documents that are just managed sheet files...
           MSPos := Pos('MANAGED', UpperCase(Document.DM_FullPath));
           HNPos := Pos('HARNESS', UpperCase(Document.DM_FullPath));
           If (MSPos >= 1) && (HNPos < 1) then
           Begin
                ManagedSheetList.Add(Document.DM_FullPath);
           End;

        End;
        Writeln(ReportFile);
    End;
    CloseFile(ReportFile);

    ManagedSheetList.SaveToFile(MSFileName);

    ReportDocument := Client.OpenDocument('Text', FileName);
    If ReportDocument <> Nil Then
        Client.ShowDocument(ReportDocument);

    MSLDocument := Client.OpenDocument('Text', MSFileName);
    If MSLDocument <> Nil Then
        Client.ShowDocument(MSLDocument);

    ManagedSheetList.Free;

End;
{..............................................................................}

{..............................................................................}
