using System;
using System.Collections.Generic;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;
using DXP;
using EDP;
using SCH;
using PCB;


public class Commands 
{
        public void Command_CountPinsOfSymbol(IServerDocumentView view, ref string parameters)
        {
            CountPinsOfSymbol();
        }
    
        public void Command_CountFootprintPrimitives(IServerDocumentView view, ref string parameters)
        {

            CountPrimitivesOfFootprint();
        }
        
    
        public void Command_CleanupSamtecSymbols(IServerDocumentView view, ref string parameters)
        {
      
            CleanUpSamtecSymbols();
        }

        public void Command_AddCourtyard(IServerDocumentView view, ref string parameters)
        {
            AddCourtyard();
        }


        public void Command_AddCenterMark(IServerDocumentView view, ref string parameters)
        {
            AddCenterMark();
        }

        public void Command_RemoveSymbolVaultLink(IServerDocumentView view, ref string parameters)
        {
            RemoveSymbolVaultLink();
        }

        public void Command_CleanupSamtecFootprints(IServerDocumentView view, ref string parameters)
        {
            CleanUpSamtecFootprints();
        }

        private bool CheckKindSchLib(IServerDocumentView ArgView)
        {
            if (ArgView != null)
            {
                IServerDocument OwnerDoucment = ArgView.GetOwnerDocument();
                if (!"SCHLIB".Equals(OwnerDoucment.GetKind(), StringComparison.OrdinalIgnoreCase))
                {
                    DXP.Utils.ShowWarning("This is not a schmatic library doucment");
                    return false;
                }
            }
            return true;
        }

        private void CleanUpPin(SCH.ISch_Pin PinObj)
            {
                int pinLenght = EDP.Utils.MilsToCoord(200); //pin length is 20 in library
                PinObj.SetState_PinLength(pinLenght);

                PinObj.SetState_ShowName(false);
                
                PinObj.SetState_Designator_CustomFontID(1); //font is Time New Roman, 10
                PinObj.SetState_Name_CustomFontID(1);

                Point pinLocation = PinObj.GetState_Location();
                pinLocation.X = Convert.ToInt32( Math.Round(Convert.ToDouble(pinLocation.X / 1000000))) * 1000000;
                pinLocation.Y = Convert.ToInt32(Math.Round(Convert.ToDouble(pinLocation.Y / 1000000))) * 1000000;
                PinObj.SetState_Location(pinLocation);
            }

        private void RemoveParameter(SCH.ISch_Parameter ParamObj, SCH.ISch_Component LibraryComponent)
        {
            if (ParamObj.GetState_Name().Equals("Comment", StringComparison.OrdinalIgnoreCase))
            {
                ParamObj.SetState_Text("*");
            }
            else LibraryComponent.RemoveSchObject(ParamObj);
                       
        }


        private void RemoveLinkedModel(SCH.ISch_Implementation SchImpl, SCH.ISch_Component LibraryComponent)
        {
            LibraryComponent.RemoveSchImplementation(SchImpl);
        }

        private OpenFileDialog InitFileOpenDialog(string DocumentKind)
        {
            OpenFileDialog FileOpenDialog = new OpenFileDialog();
            FileOpenDialog.RestoreDirectory = true;
            FileOpenDialog.Multiselect = true;

            switch(DocumentKind)
            {
                case "SCHLIB": FileOpenDialog.Filter = "Sch Library|*.SchLib"; break;
                case "PCBLIB": FileOpenDialog.Filter = "Pcb Library|*.PcbLib"; break;
            }
            
            if (FileOpenDialog.ShowDialog() == DialogResult.OK)
            {
                return FileOpenDialog;
            }
            else return null;
        }

        
        private void CleanUpSamtecSymbols()
        {
            OpenFileDialog openDialog = InitFileOpenDialog("SCHLIB");
            if (openDialog == null)
            {
                return;
            }

            IClient client = DXP.GlobalVars.Client;

            string[] SchFiles = openDialog.FileNames;
            foreach (string SchFile in SchFiles)
            {                     
                IServerDocument SchDocument = client.OpenDocument("SCHLIB", SchFile);
                if (SchDocument == null)
                    return;

                client.ShowDocumentDontFocus(SchDocument);
                ISch_ServerInterface SchServer = SCH.GlobalVars.SchServer;
                ISch_Lib currentLib = SchServer.GetCurrentSchDocument() as ISch_Lib;

                if (currentLib.LibIsEmpty())
                {
                    DXP.Utils.ShowWarning("SCH library is empty");
                    return;
                }

                ISch_Iterator LibIterator = currentLib.SchLibIterator_Create();
                LibIterator.AddFilter_ObjectSet(new SCH.TObjectSet(SCH.TObjectId.eSchComponent));

                ISch_Component LibCmp = LibIterator.FirstSchObject() as ISch_Component;
                while (LibCmp != null)
                {
                    LibCmp.SetState_ComponentDescription("");

                    ISch_Iterator ObjIterator = LibCmp.SchIterator_Create();
                    ISch_BasicContainer SchObj = ObjIterator.FirstSchObject();
                    while (SchObj != null)
                    {
                        switch (SchObj.GetState_ObjectId())
                        {
                            case SCH.TObjectId.ePin: CleanUpPin(SchObj as ISch_Pin); break;
                            case SCH.TObjectId.eParameter: RemoveParameter(SchObj as ISch_Parameter, LibCmp); break;
                            case SCH.TObjectId.eImplementation: RemoveLinkedModel(SchObj as ISch_Implementation, LibCmp); break;
                        }

                        SchObj = ObjIterator.NextSchObject();
                    }

                    LibCmp.SchIterator_Destroy(ref ObjIterator);

                    LibCmp = LibIterator.NextSchObject() as ISch_Component;
                }

                currentLib.SchIterator_Destroy(ref LibIterator);
            }

        }

        private void RemoveSymbolVaultLink()
        {
            OpenFileDialog openDialog = InitFileOpenDialog("SCHLIB");
            if (openDialog == null)
            {
                return;
            }

            IClient client = DXP.GlobalVars.Client;

            string[] SchFiles = openDialog.FileNames;
            foreach (string SchFile in SchFiles)
            {
                IServerDocument SchDocument = client.OpenDocument("SCHLIB", SchFile);
                if (SchDocument == null)
                    return;

                client.ShowDocumentDontFocus(SchDocument);
                ISch_ServerInterface SchServer = SCH.GlobalVars.SchServer;
                ISch_Lib currentLib = SchServer.GetCurrentSchDocument() as ISch_Lib;

                currentLib.SetState_FolderGUID("");
                currentLib.SetState_LifeCycleDefinitionGUID("");
                currentLib.SetState_ReleaseVaultGUID("");
                currentLib.SetState_RevisionNamingSchemeGUID("");

                if (currentLib.LibIsEmpty())
                {
                    DXP.Utils.ShowWarning("SCH library is empty");
                    return;
                }

                ISch_Iterator LibIterator = currentLib.SchLibIterator_Create();
                LibIterator.AddFilter_ObjectSet(new SCH.TObjectSet(SCH.TObjectId.eSchComponent));

                ISch_Component LibCmp = LibIterator.FirstSchObject() as ISch_Component;
                while (LibCmp != null)
                {
                    LibCmp.SetState_ComponentDescription("");
                    LibCmp.SetState_SymbolItemGUID("");
                    LibCmp.SetState_SymbolRevisionGUID("");
                    LibCmp.SetState_SymbolVaultGUID("");
                    LibCmp.SetState_VaultGUID("");
                    
                    
                    LibCmp = LibIterator.NextSchObject() as ISch_Component;
                }

                currentLib.SchIterator_Destroy(ref LibIterator);
            }

        }


        public struct PrimitiveArea
        {
            public SPoint TopLeft, TopRight, BottomLeft, BottomRight;
        }

        private PrimitiveArea CalTrackArea(IPCB_Track PcbTrack)
        {
            PrimitiveArea TrackArea = new PrimitiveArea();
            int x1 = Math.Min(PcbTrack.GetState_X1(), PcbTrack.GetState_X2());
            int x2 = Math.Max(PcbTrack.GetState_X1(), PcbTrack.GetState_X2());
            int y1 = Math.Min(PcbTrack.GetState_Y1(), PcbTrack.GetState_Y2());
            int y2 = Math.Max(PcbTrack.GetState_Y1(), PcbTrack.GetState_Y2());

            TrackArea.BottomLeft.X = x1;
            TrackArea.BottomLeft.Y = y1;
            TrackArea.BottomRight.X = x2;
            TrackArea.BottomRight.Y = y1;
            TrackArea.TopLeft.X = x1;
            TrackArea.TopLeft.Y = y2;
            TrackArea.TopRight.X = x2;
            TrackArea.TopRight.Y = y2;

            return TrackArea;
        }

        private PrimitiveArea CalArcArea(IPCB_Arc PcbArc)
        {
            PrimitiveArea ArcArea = new PrimitiveArea();


            return ArcArea;
        }

        
        private PrimitiveArea CalPadArea(IPCB_Pad PcbPad)
        {
            int Pad_X_Size, Pad_Y_Size;
            SPoint location = new SPoint();
            location.X = PcbPad.GetState_XLocation();
            location.Y = PcbPad.GetState_YLocation();

            if ((PcbPad.GetState_Rotation() == (double) 90) || (PcbPad.GetState_Rotation() == (double)270))
            {
                Pad_X_Size = PcbPad.GetState_TopYSize();
                Pad_Y_Size = PcbPad.GetState_TopXSize();
            }

            else
            {
                Pad_X_Size = PcbPad.GetState_TopXSize();
                Pad_Y_Size = PcbPad.GetState_TopYSize();
            }

            PrimitiveArea PadArea = new PrimitiveArea();
            PadArea.BottomLeft.X = location.X - (Pad_X_Size / 2);
            PadArea.BottomLeft.Y = location.Y - (Pad_Y_Size / 2);
            PadArea.BottomRight.X = location.X + (Pad_X_Size / 2);
            PadArea.BottomRight.Y = PadArea.BottomLeft.Y;
            PadArea.TopLeft.X = PadArea.BottomLeft.X;
            PadArea.TopLeft.Y = location.Y + (Pad_Y_Size / 2);
            PadArea.TopRight.X = PadArea.BottomRight.X;
            PadArea.TopRight.Y = PadArea.TopLeft.Y;

            return PadArea;
        }

        private PrimitiveArea CalComponentArea(List<PrimitiveArea> PcbPrimitiveAreas)
        {
            PrimitiveArea CmpArea = new PrimitiveArea();

            CmpArea.TopLeft.X = PcbPrimitiveAreas[0].TopLeft.X;
            CmpArea.TopLeft.Y = PcbPrimitiveAreas[0].TopLeft.Y;
            CmpArea.TopRight.X = PcbPrimitiveAreas[0].TopRight.X;
            CmpArea.TopRight.Y = PcbPrimitiveAreas[0].TopRight.Y;
            CmpArea.BottomLeft.X = PcbPrimitiveAreas[0].BottomLeft.X;
            CmpArea.BottomLeft.Y = PcbPrimitiveAreas[0].BottomLeft.Y;
            CmpArea.BottomRight.X = PcbPrimitiveAreas[0].BottomRight.X;
            CmpArea.BottomRight.Y = PcbPrimitiveAreas[0].BottomRight.Y;

            foreach (PrimitiveArea ObjArea in PcbPrimitiveAreas)
            {               
                if (ObjArea.BottomLeft.X < CmpArea.BottomLeft.X)
                {
                    CmpArea.BottomLeft.X = ObjArea.BottomLeft.X;
                    CmpArea.TopLeft.X = CmpArea.BottomLeft.X;
                }
                    
                if (ObjArea.BottomLeft.Y < CmpArea.BottomLeft.Y)
                {
                    CmpArea.BottomLeft.Y = ObjArea.BottomLeft.Y;
                    CmpArea.BottomRight.Y = CmpArea.BottomLeft.Y;
                }
                    
                if (ObjArea.TopRight.X > CmpArea.TopRight.X)
                {
                    CmpArea.TopRight.X = ObjArea.TopRight.X;
                    CmpArea.BottomRight.X = CmpArea.TopRight.X;
                }

                if (ObjArea.TopRight.Y > CmpArea.TopRight.Y)
                {
                    CmpArea.TopRight.Y = ObjArea.TopRight.Y;
                    CmpArea.TopLeft.Y = ObjArea.TopRight.Y;
                }

            }

            return CmpArea;
        }
        
        private void SetTrackLocaton(IPCB_Track PcbTrack, int ArgX1, int ArgY1, int ArgX2, int ArgY2)
        {
            if (PcbTrack == null)
                return;
            
            PcbTrack.SetState_X1(ArgX1);
            PcbTrack.SetState_Y1(ArgY1);
            PcbTrack.SetState_X2(ArgX2);
            PcbTrack.SetState_Y2(ArgY2);
        }


        private void DrawAreaAsCourtyard(PrimitiveArea Area, IPCB_ServerInterface ArgPcbServer, IPCB_Board ArgPcbBoard)
        {
            int CourtyardClearnce_IPC_L = EDP.Utils.MMsToCoord((double) 0.1);
            int lineWidth = EDP.Utils.MMsToCoord((double)0.05);
            V7_Layer MechLayer15 = new V7_Layer().Mechanical15();

            ArgPcbServer.PreProcess();

            IPCB_Track trackLeft = ArgPcbServer.PCBObjectFactory(PCB.TObjectId.eTrackObject, TDimensionKind.eNoDimension, PCB.TObjectCreationMode.eCreate_GlobalCopy) as IPCB_Track;
            SetTrackLocaton(trackLeft, Area.BottomLeft.X - CourtyardClearnce_IPC_L, Area.BottomLeft.Y - CourtyardClearnce_IPC_L, Area.TopLeft.X - CourtyardClearnce_IPC_L, Area.TopLeft.Y + CourtyardClearnce_IPC_L);
            trackLeft.SetState_Width(lineWidth);
            trackLeft.SetState_Layer((int)MechLayer15.ID);

            IPCB_Track trackRight = ArgPcbServer.PCBObjectFactory(PCB.TObjectId.eTrackObject, TDimensionKind.eNoDimension, PCB.TObjectCreationMode.eCreate_GlobalCopy) as IPCB_Track;
            SetTrackLocaton(trackRight, Area.BottomRight.X + CourtyardClearnce_IPC_L, Area.BottomRight.Y - CourtyardClearnce_IPC_L, Area.TopRight.X + CourtyardClearnce_IPC_L, Area.TopRight.Y + CourtyardClearnce_IPC_L);
            trackRight.SetState_Width(lineWidth);
            trackRight.SetState_Layer((int)MechLayer15.ID);

            IPCB_Track trackTop = ArgPcbServer.PCBObjectFactory(PCB.TObjectId.eTrackObject, TDimensionKind.eNoDimension, PCB.TObjectCreationMode.eCreate_GlobalCopy) as IPCB_Track;
            SetTrackLocaton(trackTop, Area.TopLeft.X - CourtyardClearnce_IPC_L, Area.TopLeft.Y + CourtyardClearnce_IPC_L, Area.TopRight.X + CourtyardClearnce_IPC_L, Area.TopRight.Y + CourtyardClearnce_IPC_L);
            trackTop.SetState_Width(lineWidth);
            trackTop.SetState_Layer((int)MechLayer15.ID);

            IPCB_Track trackBottom = ArgPcbServer.PCBObjectFactory(PCB.TObjectId.eTrackObject, TDimensionKind.eNoDimension, PCB.TObjectCreationMode.eCreate_GlobalCopy) as IPCB_Track;
            SetTrackLocaton(trackBottom, Area.BottomLeft.X - CourtyardClearnce_IPC_L, Area.BottomLeft.Y - CourtyardClearnce_IPC_L, Area.BottomRight.X + CourtyardClearnce_IPC_L, Area.BottomRight.Y - CourtyardClearnce_IPC_L);
            trackBottom.SetState_Width(lineWidth);
            trackBottom.SetState_Layer((int)MechLayer15.ID);

            ArgPcbBoard.AddPCBObject(trackBottom);
            ArgPcbBoard.AddPCBObject(trackLeft);
            ArgPcbBoard.AddPCBObject(trackRight);
            ArgPcbBoard.AddPCBObject(trackTop);

            ArgPcbServer.PostProcess();
            DXP.Utils.RunCommand("PCB:Zoom", "Action=Redraw");
        }


        private void AddCourtyard()
        {
            IPCB_ServerInterface PcbServer = PCB.GlobalVars.PCBServer;
            if (PcbServer == null)
                return;

            IPCB_Library PcbLib = PcbServer.GetCurrentPCBLibrary();
            if (PcbLib == null)
                return;

            IPCB_LibraryIterator LibIteartor = PcbLib.LibraryIterator_Create();
            LibIteartor.AddFilter_ObjectSet(new PCB.TObjectSet(PCB.TObjectId.eComponentObject));
            IPCB_Component PcbCmp = LibIteartor.FirstPCBObject() as IPCB_Component;

            while (PcbCmp != null)
            {
                IPCB_Board currentBoard = PcbServer.GetCurrentPCBBoard();

                IPCB_GroupIterator PcbObjItera = PcbCmp.GroupIterator_Create();
                TV6_LayerSet layers = new TV6_LayerSet(TV6_Layer.eV6_BottomLayer, TV6_Layer.eV6_BottomOverlay, TV6_Layer.eV6_Mechanical13,
                                                        TV6_Layer.eV6_TopLayer, TV6_Layer.eV6_TopOverlay);
                PcbObjItera.AddFilter_LayerSet(layers);

                IPCB_Primitive PcbObj = PcbObjItera.FirstPCBObject();

                List<PrimitiveArea> Areas = new List<PrimitiveArea>();
                while (PcbObj != null)
                {
                    PrimitiveArea ObjArea = new PrimitiveArea();

                    switch (PcbObj.GetState_ObjectID())
                    {
                        case PCB.TObjectId.ePadObject: 
                            ObjArea = CalPadArea(PcbObj as IPCB_Pad);
                            Areas.Add(ObjArea);
                            break;

                        case PCB.TObjectId.eTrackObject: 
                            ObjArea = CalTrackArea(PcbObj as IPCB_Track);
                            Areas.Add(ObjArea);
                            break;

                        case PCB.TObjectId.eArcObject:
                            break;
                    }                                        
                    
                    PcbObj = PcbObjItera.NextPCBObject();
                }

                PrimitiveArea ComponentArea = CalComponentArea(Areas);
                DrawAreaAsCourtyard(ComponentArea, PcbServer, currentBoard);

                PcbCmp.GroupIterator_Destroy(ref PcbObjItera);

                PcbCmp = LibIteartor.NextPCBObject() as IPCB_Component;
            }

            PcbLib.LibraryIterator_Destroy(ref LibIteartor);
        }


        private void AddCenterMark()
        {
            IPCB_ServerInterface PcbServer = PCB.GlobalVars.PCBServer;
            if (PcbServer == null)
                return;

            IPCB_Library PcbLib = PcbServer.GetCurrentPCBLibrary();
            if (PcbLib == null)
                return;

            IPCB_LibraryIterator LibIteartor = PcbLib.LibraryIterator_Create();
            LibIteartor.AddFilter_ObjectSet(new PCB.TObjectSet(PCB.TObjectId.eComponentObject));
            IPCB_LibComponent PcbCmp = LibIteartor.FirstPCBObject() as IPCB_LibComponent;

            while (PcbCmp != null)
            {
                IPCB_Board currentBoard = PcbServer.GetCurrentPCBBoard();

                int Origin_X = currentBoard.GetState_XOrigin();
                int Origin_Y = currentBoard.GetState_YOrigin();
                int LineWidth = EDP.Utils.MMsToCoord((double)0.1);
                int HalfLineLegnth = EDP.Utils.MMsToCoord((double)0.5);
                V7_Layer MechLayer15 = new V7_Layer().Mechanical15();

                PcbServer.PreProcess();

                IPCB_Track vLine = PcbServer.PCBObjectFactory(PCB.TObjectId.eTrackObject, TDimensionKind.eNoDimension, PCB.TObjectCreationMode.eCreate_Default) as IPCB_Track;
                SetTrackLocaton(vLine, Origin_X - HalfLineLegnth, Origin_Y, Origin_X + HalfLineLegnth, Origin_Y);
                vLine.SetState_Layer((int)MechLayer15.ID);
                vLine.SetState_Width(LineWidth);

                IPCB_Track hLine = PcbServer.PCBObjectFactory(PCB.TObjectId.eTrackObject, TDimensionKind.eNoDimension, PCB.TObjectCreationMode.eCreate_Default) as IPCB_Track;
                SetTrackLocaton(hLine, Origin_X, Origin_Y + HalfLineLegnth, Origin_X, Origin_Y - HalfLineLegnth);
                hLine.SetState_Layer((int)MechLayer15.ID);
                hLine.SetState_Width(LineWidth);

                currentBoard.AddPCBObject(vLine);
                currentBoard.AddPCBObject(hLine);

                PcbServer.PostProcess();
                DXP.Utils.RunCommand("PCB:Zoom", "Action=Redraw");

                PcbCmp = LibIteartor.NextPCBObject() as IPCB_LibComponent;
            }

            PcbLib.LibraryIterator_Destroy(ref LibIteartor);
        }

        



        private void CleanUpSamtecFootprints()
        {
            IPCB_ServerInterface PcbServer = PCB.GlobalVars.PCBServer;
            if (PcbServer == null)
                return;

            IPCB_Library PcbLib = PcbServer.GetCurrentPCBLibrary();
            if (PcbLib == null)
                return;

            IPCB_LibraryIterator LibIteartor = PcbLib.LibraryIterator_Create();
            LibIteartor.AddFilter_ObjectSet(new PCB.TObjectSet(PCB.TObjectId.eComponentObject));
            IPCB_LibComponent PcbCmp = LibIteartor.FirstPCBObject() as IPCB_LibComponent;

            PcbServer.PreProcess();

            while (PcbCmp != null)
            {               
                IPCB_Board currentBoard = PcbServer.GetCurrentPCBBoard();  // heads up, PCB Ojbect can be added only by IPCB_Board, not IPCB_Component
                
                IPCB_GroupIterator PcbObjItera = PcbCmp.GroupIterator_Create();
                IPCB_Primitive PcbObj = PcbObjItera.FirstPCBObject();
              
                while (PcbObj != null)
                {
                   switch(PcbObj.GetState_ObjectID())
                   {
                       case PCB.TObjectId.eTrackObject:
                           if ((int)PcbObj.GetState_V7Layer().ID != (int) new V7_Layer().Mechanical1().ID)
                           {
                               PcbObj = PcbObjItera.NextPCBObject();
                               continue;
                           }

                           IPCB_Track TrackObj = PcbObj as IPCB_Track;
                           TrackObj.SetState_Width(EDP.Utils.MMsToCoord((double)0.1));
                           TrackObj.SetState_Layer((int)new V7_Layer().Mechanical13().ID);
                           break;

                       case PCB.TObjectId.eArcObject:
                           if ((int)PcbObj.GetState_V7Layer().ID != (int)new V7_Layer().Mechanical1().ID)
                           {
                               PcbObj = PcbObjItera.NextPCBObject();
                               continue;
                           }

                           IPCB_Arc ArcObj = PcbObj as IPCB_Arc;
                           ArcObj.SetState_LineWidth(EDP.Utils.MMsToCoord((double)0.1));
                           ArcObj.SetState_Layer((int)new V7_Layer().Mechanical13().ID);
                           break;

                       case PCB.TObjectId.eComponentBodyObject:                           
                           IPCB_ComponentBody BodyObj = PcbObj as IPCB_ComponentBody;
                           BodyObj.SetState_Layer((int)new V7_Layer().Mechanical13().ID);
                           break;

                       case PCB.TObjectId.eTextObject:
                           PcbCmp.RemovePCBObject(PcbObj);
                           break;
                   }

                    PcbObj = PcbObjItera.NextPCBObject();
                }

                PcbServer.PostProcess();
                DXP.Utils.RunCommand("PCB:Zoom", "Action=Redraw");

                PcbCmp.GroupIterator_Destroy(ref PcbObjItera);

                PcbCmp = LibIteartor.NextPCBObject() as IPCB_LibComponent;
            }
            
            PcbLib.LibraryIterator_Destroy(ref LibIteartor);
        }


        private void CountPinsOfSymbol()
        {
            SCH.TObjectSet DontCountObject = new SCH.TObjectSet(SCH.TObjectId.eParameter, SCH.TObjectId.eDesignator);
            
            OpenFileDialog openDialog = InitFileOpenDialog("SCHLIB");
            if (openDialog == null)
            {
                return;
            }
            IClient client = DXP.GlobalVars.Client;
            string[] SymbolFiles = openDialog.FileNames;
            foreach (string SymbolFile in SymbolFiles)
            {
                //IServerDocument SymbolDocument = OpenDocuemnt(SymbolFile, "SCHLIB");
                IServerDocument SymbolDocument = client.OpenDocumentShowOrHide("SCHLIB", SymbolFile, false);
                ISch_ServerInterface SchServer = SCH.GlobalVars.SchServer;
                ISch_Lib SchLib = SchServer.GetSchDocumentByPath(SymbolFile) as ISch_Lib;
                //ISch_Lib SchLib = SchServer.GetCurrentSchDocument() as ISch_Lib;

                ISch_Iterator LibItera = SchLib.SchLibIterator_Create();
                LibItera.AddFilter_ObjectSet(new SCH.TObjectSet(SCH.TObjectId.eSchComponent));
                ISch_Component LibComp = LibItera.FirstSchObject() as ISch_Component;

                while(LibComp != null)
                {
                    string SymbolName = LibComp.GetState_SymbolReference();

                    ISch_Iterator ObjIterator = LibComp.SchIterator_Create();
                    ISch_BasicContainer SchObj = ObjIterator.FirstSchObject();

                    int PinCount = 0;
                    int PrimitiveCount = 0;

                    while (SchObj != null)
                    {
                        bool CountIt = true;

                        foreach (SCH.TObjectId ObjectKind in DontCountObject)
                        {
                            if (ObjectKind == SchObj.GetState_ObjectId())
                            {
                                CountIt = false;
                            }
                        }

                        if (SchObj.GetState_ObjectId() == SCH.TObjectId.ePin)
                        {
                            PinCount++;
                        }

                        if (CountIt) PrimitiveCount++;

                        SchObj = ObjIterator.NextSchObject();
                    }

                    LibComp.SchIterator_Destroy(ref ObjIterator);

                    System.IO.File.AppendAllText(@"G:\report.txt", SymbolName + "|" + PinCount.ToString() + "|" + PrimitiveCount.ToString() + "\r\n");

                    LibComp = LibItera.NextSchObject() as ISch_Component;
                }

                SchLib.SchIterator_Destroy(ref LibItera);

                CloseDocument(SymbolDocument);
            }
        }


        private void CountPrimitivesOfFootprint()
        {
            OpenFileDialog openDialog = InitFileOpenDialog("PCBLIB");
            if (openDialog == null)
            {
                return;
            }

            string[] FootprintFiles = openDialog.FileNames;
            foreach (string FootprintFile in FootprintFiles)
            {
                System.Threading.Thread.Sleep(5000);

                IServerDocument PcbDocuemnt = OpenDocuemnt(FootprintFile, "PCBLIB");
                if (PcbDocuemnt == null)
                {
                    DXP.Utils.ShowMessage("Failed to open " + FootprintFile);
                    return;
                }

                IPCB_ServerInterface PcbServer = PCB.GlobalVars.PCBServer;
                IPCB_Library PcbLib = PcbServer.GetCurrentPCBLibrary();

                IPCB_Board currentBoard = PcbServer.GetCurrentPCBBoard();
                currentBoard.GraphicalView_ZoomRedraw();

                IPCB_LibraryIterator LibIteartor = PcbLib.LibraryIterator_Create();
                LibIteartor.AddFilter_ObjectSet(new PCB.TObjectSet(PCB.TObjectId.eComponentObject));
                IPCB_LibComponent PcbCmp = LibIteartor.FirstPCBObject() as IPCB_LibComponent;

                while (PcbCmp != null)
                {
                    string FootprintDescription = PcbCmp.GetState_Description();
                    string FootprintName = PcbCmp.GetState_Pattern();

                    IPCB_GroupIterator PcbObjItera = PcbCmp.GroupIterator_Create();
                    int count = 0;
                    IPCB_Primitive PcbObj = PcbObjItera.FirstPCBObject();

                    while (PcbObj != null)
                    {
                        count++;
                        PcbObj = PcbObjItera.NextPCBObject();
                    }

                    PcbCmp.GroupIterator_Destroy(ref PcbObjItera);

                    System.IO.File.AppendAllText(@"G:\report.txt", FootprintName + "|" + FootprintDescription + "|" + count.ToString() + "\r\n");
                   
                    PcbCmp = LibIteartor.NextPCBObject() as IPCB_LibComponent;
                }
                
                PcbLib.LibraryIterator_Destroy(ref LibIteartor);

                CloseDocument(PcbDocuemnt);
            }

        }


        private void CloseDocument(IServerDocument ArgDocument)
        {
            IClient client = DXP.GlobalVars.Client;
            client.HideDocument(ArgDocument);
            client.CloseDocument(ArgDocument);

        }


        private IServerDocument OpenDocuemnt(string DocumentPath, string DocumentKind)
        {
            IClient client = DXP.GlobalVars.Client;

            try
            {
                IServerDocument document = client.OpenDocumentShowOrHide(DocumentKind, DocumentPath, false);
                client.ShowDocumentDontFocus(document);

                return document;
            }

            catch (ExternalException e)
            {
                //DXP.Utils.ShowMessage(e.Message);
                return null;
            }                     
        }

        
}

