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
		public void Command_CleanupSamtecSymbols(IServerDocumentView view, ref string parameters)
        {
            if (CheckKindSchLib(view))
            {
                CleanUpSamtecSymbols();
            }
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

        private OpenFileDialog InitSchFileOpenDialog()
        {
            OpenFileDialog SchLibOpenDialog = new OpenFileDialog();
            SchLibOpenDialog.RestoreDirectory = true;
            SchLibOpenDialog.Multiselect = true;
            SchLibOpenDialog.Filter = "Sch Library|*.SchLib";
            if (SchLibOpenDialog.ShowDialog() == DialogResult.OK)
            {
                return SchLibOpenDialog;
            }
            else return null;
        }

        
        private void CleanUpSamtecSymbols()
        {
            
            ISch_ServerInterface SchServer = SCH.GlobalVars.SchServer;
            if (SchServer == null)
                return;

            ISch_Lib currentLib = SchServer.GetCurrentSchDocument() as ISch_Lib;
            if (currentLib == null)
                return;

            if(currentLib.LibIsEmpty())
            {
                DXP.Utils.ShowWarning("SCH library is empty");
                return;
            }

            ISch_Iterator LibIterator = currentLib.SchLibIterator_Create();
            LibIterator.AddFilter_ObjectSet(new SCH.TObjectSet(SCH.TObjectId.eSchComponent));

            ISch_Component LibCmp = LibIterator.FirstSchObject() as ISch_Component;
            while(LibCmp != null)
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

