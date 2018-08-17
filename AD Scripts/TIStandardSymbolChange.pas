{..............................................................................}
Var
Project                     :  IProject;
Document                    :  IDocument;
SchLib                      :  ISch_Lib;
PinCount                    :  Integer;
MaxCount                    :  Integer;
ReportInfo                  :  TStringList;
Procedure CalculateWidth(PinArray : Isch_Pin, Rectangle : ISch_Rectangle);
Var
CharacterCount    : Integer;
i, j, k           : Integer;
PinName           : WideString;
Begin
    CharacterCount := 0;
    For i := 0 to PinCount - 1 Do
    Begin
        CharacterCount := 0;
        For j := 0 to PinCount - 1 Do
        Begin
            If (PinArray[i].Location.y = PinArray[j].Location.y)
            && (PinArray[i].Location.x <> PinArray[j].Location.x)
            && (PinArray[i].OwnerPartDisplayMode = PinArray[j].OwnerPartDisplayMode)
            && (PinArray[i].OwnerPartId = Rectangle.OwnerPartId)
            && (PinArray[j].OwnerPartId = Rectangle.OwnerPartId)  Then
            Begin
                PinName :=   PinArray[i].Name;
                for k := 1 to  Length(PinName) Do
                Begin
                    If PinName[k] <> '\' Then CharacterCount := CharacterCount + 1;
                End;
                PinName := PinArray[j].Name;
                for k   := 1 to  Length(PinName) Do
                Begin
                    If PinName[k] <> '\' Then CharacterCount := CharacterCount + 1;
                End;
                    If MaxCount < CharacterCount Then MaxCount := CharacterCount;
            End;
        End;
    End;
End;
Procedure ChangeSymbolWidth(PinArray : Isch_Pin; Rectangle : Isch_Rectangle;LibComp : ISch_Component);
Var
SymbolWidth       : Integer;
SymbolHeight      : Integer;
i                 : Integer;
Location          : Tlocation;
MinWidth          : Integer;
MinHeight         : Integer;
MinX              : Integer;
MinY              : Integer;
MaxX              : Integer;
MaxY              : Integer;
CenterLocationX   : Integer;
CenterLocationY   : Integer;

Begin
    SymbolWidth := (MaxCount*800000 + 3000000);
    SymbolWidth := ((SymbolWidth Div 2000000) + 1) * 2000000;
    SymbolHeight:= Rectangle.Corner.y - Rectangle.Location.y + 1000000;
    If SymbolHeight mod 2000000 <>0 then SymbolHeight:=((SymbolHeight Div 2000000) + 1)*2000000;
    SchServer.RobotManager.SendMessage(Rectangle.I_ObjectAddress, c_BroadCast, SCHM_BeginModify, c_NoEventData);
    MinWidth := 8000000;
    MinHeight:= 6000000;
    If SymbolWidth <= MinWidth Then SymbolWidth := MinWidth;
    If SymbolHeight <= MinHeight Then SymbolHeight :=MinHeight;
    CenterLocationX:=SymbolWidth/2;
    CenterLocationY:=SymbolHeight/2;
    Location   := Rectangle.Location;
    Location.x := -CenterLocationX;
    Location.y := -CenterLocationY;
    Rectangle.SetState_Location(Location);
    Location   := Rectangle.Corner;
    Location.x := CenterLocationX;
    Location.y := CenterLocationY;
    Rectangle.SetState_Corner(Location);
    For i := 0 to PinCount - 1 Do
    Begin
        If (PinArray[i].Orientation = 0)
        && (PinArray[i].OwnerPartId = Rectangle.OwnerPartId) Then
        Begin
            Location   := PinArray[i].Location;
            Location.x := Rectangle.Corner.x;
            PinArray[i].SetState_Location(Location);
        End;
        If (PinArray[i].Orientation = 2)
        && (PinArray[i].OwnerPartId = Rectangle.OwnerPartId) Then
        Begin
            Location   := PinArray[i].Location;
            Location.x := Rectangle.Location.x;
            PinArray[i].SetState_Location(Location);
        End;
        If ((PinArray[i].Orientation =0)||(PinArray[i].Orientation =2)) && (PinArray[i].OwnerPartId = Rectangle.OwnerPartId)&&(PinArray[i].OwnerPartDisplayMode = Rectangle.OwnerPartDisplayMode) Then
        Begin
            Location.y := PinArray[i].Location.y + CenterLocationY - 1000000;
            PinArray[i].Setstate_Location(Location);
       End;
       MaxCount := Nil;
    End;
    SchServer.RobotManager.SendMessage(Rectangle.I_ObjectAddress, c_BroadCast, SCHM_EndModify, c_NoEventData);
End;
Procedure TIStandardSymbolChange;
var
i,j                         :  Integer;
LibIterator                 :  ISch_Iterator;
LibComp                     :  ISch_Component;
SCHRect                     :  ISch_Rectangle;
RectIterator                :  ISch_Rectangle;
PinIterator                 :  ISCH_Iterator;
RIterator                   :  ISch_Iterator;
Pins                        :  Array[0..4000] of ISch_Pin;
Pin                         :  ISCH_Pin;
Width                       :  Integer;
Line                        :  ISch_Line;
LineIterator                :  ISch_Iterator;
PolyLine                    :  ISch_PolyLine;
PolyLineIterator            :  ISch_Iterator;
SchLibname                  :  String;
Label                          n1;
Begin
    ReportInfo := TStringList.Create;
    ReportInfo.Clear;
    Project := GetWorkSpace.DM_FocusedProject;
    For i   := 0 To Project.DM_LogicalDocumentCount - 1 Do
    Begin
        Document := Project.DM_LogicalDocuments(i);
        If Document.DM_DocumentKind = 'SCHLIB' Then
        Begin
            SchLib := Client.OpenDocument('SCHLIB',Document.DM_FullPath);
            Client.ShowDocument(SchLib);
            SchLib := SchServer.GetCurrentSchDocument;
            If SchLib = Nil then Exit;
            LibIterator := SchLib.SchLibIterator_Create;
            LibIterator.AddFilter_ObjectSet(MkSet(eSchComponent));
            LibComp := LibIterator.FirstSchObject;
            SchLibname:=LibComp.LibReference;
            If LibComp <> nil then
            Begin
                If LibComp.Designator.Text <> 'U?' Then Continue;
                PinIterator := Schlib.SchLibIterator_Create;
                RectIterator := SchLib.SchLibIterator_Create;
                LineIterator := SchLib.SchIterator_Create;
                PolyLineIterator := SchLib.SchIterator_Create;
                PinIterator.AddFilter_ObjectSet(MkSet(ePin));
                RectIterator.AddFilter_ObjectSet(MkSet(eRectangle));
                LineIterator.AddFilter_ObjectSet(MkSet(eLine));
                PolyLineIterator.AddFilter_ObjectSet(MkSet(ePolyLine));
                SCHRect := RectIterator. FirstSchObject;
                If SCHRect = Nil Then
                Begin
                    SchLib.SaveToFile('C:\Users\tazo\Desktop\NO Change Symbols\'+SchLibname+'.SchLib');
                    Continue;
                End;
                Line := LineIterator. FirstSchObject;
                If Line <> Nil Then
                Begin
                    SchLib.SaveToFile('C:\Users\tazo\Desktop\NO Change Symbols\'+SchLibname+'.SchLib');
                    Continue;
                End;
                PolyLine := PolyLineIterator.FirstSchObject;
                If PolyLine <> Nil Then
                Begin
                    SchLib.SaveToFile('C:\Users\tazo\Desktop\NO Change Symbols\'+SchLibname+'.SchLib');
                    Continue;
                End;
                Pin := PinIterator.FirstSchObject;
                j := 0;
                PinCount := 0;
                While Pin <> Nil Do
                Begin
                    If (Pin.Orientation = 1) or (Pin.Orientation = 3) then
                        Begin
                            ReportInfo.Add(LibComp.LibReference);
                            SchLib.SaveToFile('C:\Users\tazo\Desktop\vertical pin symbol\'+SchLibname+'.SchLib');
                            goto n1;
                        End
                    else
                       Begin
                           Pins[j] := Pin;
                           j := j+1;
                           PinCount := PinCount + 1;
                           Pin := PinIterator.NextSchObject;
                      End;
                End;
                While SCHRect <> Nil Do
                Begin
                    SCHRect.Color:=0;
                    SCHRect.LineWidth:=eSmall;
                    CalculateWidth(Pins, SCHRect);
                    ChangeSymbolWidth(Pins, SCHRect,LibComp);
                    SCHRect := RectIterator.NextSchObject;
               End;
                  SchLib.SaveToFile('C:\Users\tazo\Desktop\SCH Symbols\'+SchLibname+'.SchLib');
               n1:SchLib.SchIterator_Destroy(PinIterator);
                  SchLib.SchIterator_Destroy(RectIterator);
                  SchLib.SchIterator_Destroy(LineIterator);
                  SchLib.SchIterator_Destroy(PolyLineIterator);
           End;
           SchLib.SchIterator_Destroy(LibIterator);
           SchLib.GraphicallyInvalidate;
        End;
    End;
    ReportInfo.SaveToFile('C:\Users\tazo\Desktop\vertical pin symbol.txt');
End;

