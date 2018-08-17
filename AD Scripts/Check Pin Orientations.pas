var
    FilePath        :          TDynamicString;
    CurrentLib      :          ISCH_Lib;
    LibraryIterator :          ISch_Iterator;
    LibComp         :          ISch_Component;
    WorkSpace       :          IWorkSpace;
    Messager        :          IMessagesManager;
    ReportList      :          TStringList;
    Res             :          String;
    LineIterator     :         ISch_Iterator;
    CurrentLine      :         ISch_Line;

Function CheckLineOrientations(const LineStart: TLocation, const LineEnd: TLocation) : String;
Begin
     If (LineStart.X = LineEnd.X) Then Result := 'Vertical'
        Else If (LineStart.Y = LineEnd.Y) Then Result := 'Horizontal'
             Else Result := Null;
     If (LineStart.X = LineEnd.X && LineStart.Y = LineEnd.Y) Then Result := Null;
end;

Function TestLine(const ALine : ISch_Line);
Begin

     ShowMessage(IntToStr(ALine.Location.X));
End;


Procedure StartToCheck;
Begin
     ResetParameters;
     AddStringParameter('Dialog', 'FileOpenSave');
     AddStringParameter('Mode' , '0');
     AddStringParameter('FileType1' , 'Schematic Library(*.schlib)|*.schlib');
     RunProcess('Client:RunCommonDialog');

     GetStringParameter('Result' , Res);
     If (Res = 'True') Then
     Begin
         GetStringParameter('Path' , FilePath);
     End
     else exit;

     CurrentLib := Client.OpenDocument('SCHLIB', FilePath);
     Client.ShowDocument(CurrentLib);
     CurrentLib := SCHServer.GetCurrentSchDocument;

     LibraryIterator := CurrentLib.SchLibIterator_Create;
     LibraryIterator.AddFilter_ObjectSet(MkSet(eSchComponent));
     LibComp := LibraryIterator.FirstSchObject;

     LineIterator := LibComp.SchIterator_Create;
     LineIterator.AddFilter_ObjectSet(MkSet(eLine));
     CurrentLine := LineIterator.FirstSchObject;
     If (CurrentLine <> Nil) Then
     Begin
     TestLine(CurrentLine);
     End;
     LibComp.SchIterator_Destroy(LineIterator);
End;
