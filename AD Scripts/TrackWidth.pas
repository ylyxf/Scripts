Procedure TrackWidth;
Var
   Width : Float;
   Board : IPCB_Board;
   Iterator :  IPCB_BoardIterator;
   Track : IPCB_Track;
   I : Integer;
Begin
    Width := 1;
    I := 0;
    Board := PCBServer.GetCurrentPCBBoard;
    If Board = Nil Then Exit;

    Iterator := Board.BoardIterator_Create;
    Iterator.AddFilter_ObjectSet(MkSet(eTrackObject));
    Iterator.AddFilter_LayerSet(MkSet(eMechanical1));
    Track := Iterator.FirstPCBObject;

    While (Track <> Nil) Do
          Begin
               Width := CoordToMms(Track.Width)  ;
               if Width <> 0.2 Then   i:=1;
               Track := Iterator.NextPCBObject;
          End;
    Board.BoardIterator_Destroy(Iterator);
    ShowInfo ('The number of ports on the current schematic is : ' +
               FloatToStr(i));
End;
