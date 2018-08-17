using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using Altium.Sdk.DxpAppServer;
using Altium.Sdk.DxpAppServer.PartCatalog;
using Altium.Sdk.DxpAppServer.IDSServiceProxy;
using Ionic.Zip;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

namespace test
{
    class GetVaultInfo
    {
        public const string vaultAdress = "http://vault.live.altium.com";
 
        static void Main(string[] args)
        {
            try
            {
                GetVaultInfo test = new GetVaultInfo();
                //testConnectwithSessionID("E6E515C6-2333-408D-ABC4-0805881B6986", vaultAdress);
                //connectVault(vaultAdress, "frank.qiu@altium.com", "123456");
                //testVault();

                VaultClient client = test.connectPublicVault();
                //test.countItem(client);

                //VaultClient client = test.connectVault("http://shacontent-vat.altium.biz:9780", "admin", "admin");
                test.countAllCommponents(client);

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

        }

        static void testScript()
        {
            ScriptEngine engine = Python.CreateEngine();
            ScriptScope scope = engine.CreateScope();
            ScriptSource script = engine.CreateScriptSourceFromFile(@"buildCmpLib.py");

            var paths = engine.GetSearchPaths();
            string dir = @"C:\Program Files (x86)\IronPython 2.7\Lib\";
            paths.Add(dir);
            engine.SetSearchPaths(paths);

            scope.SetVariable("crPath", @"G:\Scripts\Python\Vault Release Tool\cmpLib_ipy\Diode.csv");
            scope.SetVariable("cmpLibPath", @"G:\b\result.cmplib");
            scope.SetVariable("crType", "TI");
            scope.SetVariable("vaultAddress", "http://shacontent-vat.altium.biz:9780");
            scope.SetVariable("userName", "admin");
            scope.SetVariable("pwd", "admin");

            try
            {
                var scriptResult = script.Execute(scope);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static void testVault()
        {
            string loginURL = "http://ids.live.altium.com/?cls=soap";
            IDSClient idsClient = new IDSClient(loginURL);
            IDSLoginResult loginResult = idsClient.Login("frank.qiu@altium.com", "123456", false, LoginOptions.KillExistingSession);
            string vaultURL = "http://vault.live.altium.com/?cls=soap";
            VaultClient vaultClient = new VaultClient(vaultURL);
            vaultClient.Login(loginResult.SessionId);
            Console.WriteLine("Session ID = " + vaultClient.SessionID);
            Console.WriteLine("Vault HRID = " + vaultClient.VaultInfo.HRID);
            Console.WriteLine("Vault Serivce URL = " + vaultClient.ServiceURL);
            //VaultFolderList folderlist = vaultClient.GetAllFolders();

            try
            {
                VaultItemRevisionList itemRevisions = vaultClient.GetItemRevisions("COMMENT = 'RES-2'", new VaultRequestOptions() { VaultRequestOption.IncludeAllChildObjects });
                if (itemRevisions.Count > 0)
                {
                    foreach (VaultItemRevision itemRevision in itemRevisions)
                    {
                        Console.WriteLine(itemRevision.Comment + " " + itemRevision.GUID);
                    }
                }
                else { Console.WriteLine("not found"); }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }
        }

        private VaultClient connectVault(string vaultAddress, string userName, string password)
        {
            string loginURL = vaultAddress + "/ids/?cls=soap";
            IDSClient idsClient = new IDSClient(loginURL);
            IDSLoginResult loginResult = idsClient.Login(userName, password, false);

            string vaultURL = vaultAddress + "/vault/?cls=soap";
            VaultClient vaultClient = new VaultClient(vaultURL);
            vaultClient.Login(loginResult.SessionId);

            Console.WriteLine("Session ID = " + vaultClient.SessionID);
            Console.WriteLine("Vault HRID = " + vaultClient.VaultInfo.HRID);
            Console.WriteLine("Vault Serivce URL = " + vaultClient.ServiceURL);

            return vaultClient;
        }

        static void testConnectwithSessionID(string sessionID, string vaultAddress)
        {
            string vaultURL = vaultAdress + "/vault/?cls=soap";
            VaultClient vaultClient = new VaultClient(vaultURL);
            vaultClient.Login(sessionID);
            Console.WriteLine("Session ID = " + vaultClient.SessionID);
            Console.WriteLine("Vault HRID = " + vaultClient.VaultInfo.HRID);
            Console.WriteLine("Vault Serivce URL = " + vaultClient.ServiceURL);
        }

        private VaultClient connectPublicVault()
        {
            string loginURL = "http://ids.live.altium.com/?cls=soap";
            IDSClient idsClient = new IDSClient(loginURL);
            IDSLoginResult loginResult = idsClient.Login("frank.qiu@altium.com", "123456", false, LoginOptions.KillExistingSession);
            string vaultURL = "http://vault.live.altium.com/?cls=soap";
            VaultClient vaultClient = new VaultClient(vaultURL);
            vaultClient.Login(loginResult.SessionId);
            Console.WriteLine("Session ID = " + vaultClient.SessionID);
            Console.WriteLine("Vault HRID = " + vaultClient.VaultInfo.HRID);
            Console.WriteLine("Vault Serivce URL = " + vaultClient.ServiceURL);

            return vaultClient;
        }
        
        private int countItem(VaultClient vaultClient)
        {
            int itemCount = vaultClient.GetItemRevisionCount("COMMENT = 'RES-2' AND FOLDERGUID = 'XXXXXXX'");
            Console.WriteLine("Count is " + itemCount.ToString());

            return itemCount;
        }

        private void countAllCommponents(VaultClient vaultClient)
        {
            VaultFolderList folderList = vaultClient.GetAllFolders();
            IDictionary<string,string> pathsList = buildfoldersPath(folderList);

            List<string> resultList = new List<string>();
            foreach (VaultFolder folder in folderList)
            {
                if (folder.FolderTypeGUID == "89B6B381-D64E-456E-BF2A-E08CBB186A84")
                {
                    int itemCount = vaultClient.GetItemCount(string.Format("FOLDERGUID = '{0}'",folder.GUID));
                    string line = pathsList[folder.GUID] + "   " + itemCount.ToString();
                    resultList.Add(line);
                    Console.WriteLine(line);
                }
            }

            System.IO.File.WriteAllLines(@"result.txt", resultList);
        }

        private IDictionary<string,string> buildfoldersPath(VaultFolderList folderList)
        {
            Dictionary<string, string> foldersPath = new Dictionary<string, string>();

            foreach(VaultFolder folder in folderList)
            {
                string folderPath = folder.HRID;
              
                if (folder.ParentFolderGUID != "")
                {
                    VaultFolder nextNode = folder;
                    while (nextNode.ParentFolderGUID != "")
                    {
                       
                        VaultFolder parentFolder = matchParentFolder(nextNode, folderList);
                        if (parentFolder != null)
                        {
                            folderPath = parentFolder.HRID + "/" + folderPath;
                            nextNode = parentFolder;
                        }
                        else break;
                    }
                }
               
                foldersPath.Add(folder.GUID, folderPath);
                //Console.WriteLine(folderPath);
            }
           
            return foldersPath;
        }

        private VaultFolder matchParentFolder(VaultFolder childFolder, VaultFolderList allFolder)
        {
            VaultFolder parentFolder = null;
            foreach(VaultFolder folder in allFolder)
            {
                if(childFolder.ParentFolderGUID == folder.GUID)
                {
                    parentFolder = folder;
                    break;
                }
            }

            return parentFolder;
        }
    }
}
