Var
   Project                  :   IProject;
   Workspace                :   IWorkspace;
   i                        :   Integer;
   Document                 :   IDocument;
   CurrentLib               :   IPCB_Library;
   LibraryIterator          :   IPCB_LibraryIterator;
   PadIterator              :   IPCB_GroupIterator;
   Pad                      :   IPCB_Pad;
   LibComp                  :   IPCB_LibComponent;
   Board                    :   IPCB_Board;
   PadList                  :   TObjectList;
   TextObj                  :   IPCB_Text;
   TextObj2                  :   IPCB_Text;

Procedure ProcessLib;
Begin
     LibraryIterator := CurrentLib.LibraryIterator_Create;
     LibraryIterator.AddFilter_ObjectSet(Mkset(eComponentObject));
     LibraryIterator.SetState_FilterAll;
     LibComp := LibraryIterator.FirstPCBObject;

     While LibComp <> Nil Do
     Begin
          PCBServer.PreProcess;
          TextObj := PCBServer.PCBObjectFactory(eTextObject, eNoDimension, eCreate_Default);
          PCBServer.SendMessageToRobots(TextObj.I_ObjectAddress ,c_Broadcast, PCBM_BeginModify , c_NoEventData);
          TextObj.XLocation := MilsToCoord(500);
          TextObj.YLocation := MilsToCoord(500);
          TextObj.Layer     := eTopOverlay;
          TextObj.Text      := 'Traditional Protel Text';
          TextObj.Size       := MilsToCoord(900);   // sets the height of the text.


          LibComp.BeginModify;
          LibComp.AddPCBObject(TextObj);
          PCBServer.SendMessageToRobots(TextObj.I_ObjectAddress, c_Broadcast, PCBM_EndModify         , c_NoEventData);
          PCBServer.SendMessageToRobots(LibComp.I_ObjectAddress, c_Broadcast, PCBM_BoardRegisteration, TextObj.I_ObjectAddress);
          PCBServer.PostProcess;

          ResetParameters;
          AddStringParameter('Action', 'All');
          RunProcess('PCB:Zoom');

          ShowMessage(TextObj.Text);
          //PadList := TObjectList.Create;
         // PadIterator := LibComp.GroupIterator_Create;
          //PadIterator.AddFilter_ObjectSet(mkset(ePadObject));
         // Pad := PadIterator.FirstPCBObject;
          PadIterator := LibComp.GroupIterator_Create;
          PadIterator.AddFilter_ObjectSet(mkset(eTextObject));
          TextObj.Text := 'delete';
          TextObj2 := PadIterator.FirstPCBObject;
          ShowMessage(TextObj2.Text);
          ShowMessage(TextObj.Text);
         // While Pad <> Nil Do
          //Begin
          //     PadList.Add(Pad);
         //      Pad := PadIterator.NextPCBObject;
        //  End;

         // PCBServer.PreProcess;
         // For i := 0 to PadList.Count -1 Do
         // Begin
         //      Pad := PadList.Items(i);
        //       LibComp.RemovePCBObject(Pad);
         // End;
       //   PCBServer.PostProcess;
        //  PadList.Free;
        Client.SendMessage('PCB:Zoom', 'Action=Redraw' , 255, Client.CurrentView); 
          LibComp.GroupIterator_Destroy(PadIterator);
          LibComp := LibraryIterator.NextPCBObject;
     End;

      CurrentLib.LibraryIterator_Destroy(LibraryIterator);
End;


Procedure GetPCBLibraryDoc;
Begin

  Workspace := GetWorkSpace;
  Project :=   Workspace.DM_FocusedProject;
 // ShowMessage(Project.DM_ObjectKindString);

  For i := 0 to Project.DM_LogicalDocumentCount - 1 Do
  Begin
       Document := Project.DM_LogicalDocuments(i);

       If Document.DM_DocumentKind = 'PCBLIB' Then
       Begin
            CurrentLib := Client.OpenDocument('PCBLIB', Document.DM_FullPath);
            Client.ShowDocument(CurrentLib);
            CurrentLib := PCBServer.GetCurrentPCBLibrary;
            ProcessLib;

       End;

  End;
End ;
