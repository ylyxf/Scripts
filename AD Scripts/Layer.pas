Procedure Layers;
Var
    Board   : IPCB_Board;
    Layer   : TLayer;
    LS      : IPCB_LayerStack;
    LObject : IPCB_LayerObject;

Begin
     Board := PCBServer.GetCurrentPCBBoard;
     If Board = Nil Then Exit;
     LS := Board.LayerStack;
     If LS= Nil Then Exit;

     LObject := LS.LayerObject[eMechanical1];
     LObject.Name := 'Outline';

     LObject := LS.LayerObject[eMechanical2];
     LObject.Name := 'Printout ID';

     LObject := LS.LayerObject[eMechanical6];
     LObject.Name := 'Notes';

     LObject := LS.LayerObject[eMechanical7];
     LObject.Name := 'Component Area (Approx)';

     LObject := LS.LayerObject[eMechanical10];
     LObject.Name := 'Gerber ID';

     LObject := LS.LayerObject[eMechanical13];
     LObject.Name := 'Dimensions';

     Client.SendMessage('PCB:Zoom', 'Action=Redraw' , 255, Client.CurrentView);
End  ;
