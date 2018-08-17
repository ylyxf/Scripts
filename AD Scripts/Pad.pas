Proecdure CountPads;
Var
   Board: IPCB_Board;
   Pad: IPCB_Pad;
   Iterator: IPCB_BoardIterator;
   PadNumber: Int;
Begin
     Board:= PCBServer.GetCurrentPCBBoard;
     If Board = Nil Then Exit;

     Iterator:= Board.BoardIterator_Create;
     Iterator.AddFilter_ObjectSet(MkSet(ePadObject));
     Iterator.AddFilter_LayerSet(AllLayers);
     Iterator.AddFilter_Method(eProcessAll);

     PadNumber:= 0;
     Pad := Iterator.FirstPCBObject;
     While (Pad<> Nil) Do
     Begin
          PadNumber:= PadNumber +1;
          Pad:= Iterator.NextPCBObject;
     End;

     Board.BoardIterator_Destroy(Iterator);

     ShowMessage(IntToStr(PadNumber));
End;
