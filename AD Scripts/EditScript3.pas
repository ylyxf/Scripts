Procedure RunSpatialIteratorExample;
Var
 CurrentSheet : ISch_Document;
 SpatialIterator : ISch_Iterator;
 P,P1 : String;
 Rect : TCoordRect;
 GraphicalObj : ISch_GraphicalObject;
Begin
 // Obtain the schematic server interface and the
 // current schematic document
 If SchServer = Nil Then Exit;
 CurrentSheet := SchServer.GetCurrentSchDocument;
 If CurrentSheet = Nil Then Exit;

 // Obtain the coordinates from the corners clicked by the user.
 If Not CurrentSheet.ChooseRectangleInteractively(Rect,
 'Please select the first corner',
 'Please select the second corner') Then Exit;

 // Create a spatial iterator
 SpatialIterator := CurrentSheet.SchIterator_Create;
 If SpatialIterator = Nil Then Exit;

 Try
 // Look for components only within the defined boundary
 SpatialIterator.AddFilter_ObjectSet(MkSet(eSchComponent));
 SpatialIterator.AddFilter_Area(Rect.left, Rect.bottom, Rect.right, Rect.top);

 GraphicalObj := SpatialIterator.FirstSchObject;
 While GraphicalObj <> Nil Do
 Begin
 P1 := 'X:' + IntToStr(GraphicalObj.Location.X) +
 ', Y:' + IntToStr(GraphicalObj.Location.Y);
 P := P + P1 + #13;
 GraphicalObj := SpatialIterator.NextSchObject;
 End;
 Finally
 CurrentSheet.SchIterator_Destroy(SpatialIterator);
 End;
 ShowInfo('Component objects found at' + #13 + P);
End;
