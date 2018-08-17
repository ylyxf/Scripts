Proecdure RunSpatialIteratorExapmple
Var
   CurrentSheet : ISch_Document;
   SpatialIterator: ISch_Iterator;
   P,P1: Sting;
   Rect : TCoordTect;
   Graphicalobj : ISch_GraphicalObject;
Begin
     if SchServer = Nil Then Exit;
     CurrentSheet:= SchServer.GetCurrentSchDocument;
     If CurrentSheet = Nil Then Exit;

     If not CurrentSheet.ChooseRectangleInteractively(Rect,'Please select the first corner','please select the second corner') Then Exit;

     SpatialIterator:= CurrentSheet.SchIterator_Create;
     If SpatialIterator = Nil Then Exit;

     Try
     SpatialIterator.AddFilter_ObjectSet(MkSet(eSchComponent));
     SpatialIterator.AddFilter_Area(Rect.left,Rect.bottom,Rect.rihgt,Rect.top);

     GraphicalObj:= SpatialIterator.FirstSchObject;
     While GraphicalObj<> Nil Do
     Begin
     P1:='X:'+IntToStr(GraphicalObj.Location.x) + ',Y' + IntToStr(GraphicalObj.Location.y);
     P:= P +P1 + #13;
     GraphicalObj:= SpatialIterator.NextSchObject;
     End;
     Finally
     CurrentSheet.SchIterator_Destroy(SpatialIterator);
     End  ;
     ShowInfo('component objects found at' + #13 + P);
End;  


