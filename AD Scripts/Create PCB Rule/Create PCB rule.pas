Procedure CreateShortCircuitRule;
var
   PCBBoard                      :  IPCB_Board;
   Rule                          :  IPCB_ShortCircuitConstraint;
   Iterator                      :  IPCB_BoardIterator;
   FootprintName                 :  String;
   Footprint                     :  IPCB_Component;

Begin
     PCBBoard := PCBServer.GetCurrentPCBBoard;
     If PCBBoard = Nil Then Exit;

     Iterator := PCBBoard.BoardIterator_Create;
     Iterator.AddFilter_ObjectSet(Mkset(eComponentObject));
     Iterator.AddFilter_LayerSet(AllLayers);
     Iterator.AddFilter_Method(eProcessAll);
     Footprint := Iterator.FirstPCBObject;
     While (Footprint <> Nil) Do
     Begin
          FootprintName := Footprint.FootprintDescription;
     End;

     Rule := PCBServer.PCBRuleFactory(eRule_ShortCircuit);

     Rule.Scope1Expression := 'IsBoardCutoutRegion and ' +
                              '(HasFootprint(''ROS-119S202-40ML5_V'') or ' +
                              'HasFootprint(''ROS-119S242-40ML5_V'') or ' +
                              'HasFootprint(''ROS-18S203-40ML5_V'') or ' +
                              'HasFootprint(''ROS-18S243-40ML5_V'') or ' +
                              'HasFootprint(''ROS-19S202-40ML5_V'') or ' +
                              'HasFootprint(''ROS-19S242-40ML5_V'') or ' +
                              'HasFootprint(''ROS-28K203-40ML5_V'') or ' +
                              'HasFootprint(''ROS-28K209-40ML5_V'') or ' +
                              'HasFootprint(''ROS-32K145-400L5_V'') or ' +
                              'HasFootprint(''ROS-32K242-40ML5_V''))' ;

     Rule.Scope2Expression := 'IsVia OR IsPad';
     Rule.Name := 'ShortCircuit_BoardCutout';
     Rule.Enabled := TRUE;
     Rule.Allowed := TRUE;

     PCBBoard.AddPCBObject(Rule);
End;
