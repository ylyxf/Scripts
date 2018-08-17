Procedure Outline;

Var
   Board : IPCB_Board;
   I : Integer;
Begin
     Board := PCBServer.GetCurrentPCBBoard;
     If   Board = Nil Then Exit;

      Board.BoardOutline.Invalidate;
      Board.BoardOutline.Rebuild;
      Board.BoardOutline.Validate;

      I :=   Board.BoardOutline.PointCount;
       ShowInfo ('The number of ports on the current schematic is : ' +
               IntToStr(I));

End;
