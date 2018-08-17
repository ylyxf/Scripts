using System;
using System.Windows.Forms;
using IniParser;
using IniParser.Model;
using Altium.Sdk.DxpAppServer;
using Microsoft.Scripting.Hosting;
using IronPython.Hosting;
using System.Runtime.InteropServices;

namespace Vault_Release_Tool
{
    public partial class mainForm : Form
    {
        public IniData config;
        public VaultClient vaultClient;

        [DllImport("kernel32.dll")]
        static extern bool FreeConsole();
        [DllImport("kernel32.dll")]
        public static extern bool AllocConsole();


        public mainForm()
        {       
          
            InitializeComponent();
        }


        private void btnAddVault_Click(object sender, EventArgs e)
        {
            Add_Vault addVault = new Add_Vault(this);
            addVault.Show();
        }

        public void addVaultToList(string vaultName)
        {
            this.dlVault.Items.Add(vaultName);
        }

        private  IniData initVaultListandTextBox()
        {

            var parser = new FileIniDataParser();
            IniData vaultConfig = parser.ReadFile("Config.ini");

            Boolean vaultFound = false;
            foreach (SectionData section in vaultConfig.Sections)
            {
                if (section.SectionName != "Release Config")
                {
                    string vaultURL = section.SectionName;
                    this.addVaultToList(vaultURL);
                    vaultFound = true;
                }
                else
                {
                    this.txtCMP.Text = vaultConfig["Release Config"]["CmpLib File"];
                    this.txtCR.Text = vaultConfig["Release Config"]["Component Record"];
                    this.txtSrcFolder.Text = vaultConfig["Release Config"]["Source Folder"];
                    this.txtTarFolder.Text = vaultConfig["Release Config"]["Target Folder"];
                }
                
            }

            if (vaultFound)  this.dlVault.SelectedIndex = 0;
           
            return vaultConfig;
 
        }

        private void mainForm_Load(object sender, EventArgs e)
        {
            
            initVaultListandTextBox();
        }

        private void btnBuild_Click(object sender, EventArgs e)
        {
            try 
            {
                string vaultULR = dlVault.SelectedItem.ToString();

                if (vaultULR != "")
                {
                    AllocConsole();
                    runBuildCmpScript(vaultULR);
                    FreeConsole();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
          
            
        }

        private void runBuildCmpScript(string vaultAddress)
        {
            
                string vaultURL, crType, userName, password, crPath, cmpLibPath;

                crType= "Altium";
                if (this.rbTI.Checked)
                {
                    crType = "TI";
                }
                crPath = this.txtCR.Text;
                cmpLibPath = this.txtCMP.Text;

                vaultURL = vaultAddress;
                var parser = new FileIniDataParser();
                IniData vaultConfig = parser.ReadFile("Config.ini");
                userName = vaultConfig[vaultURL]["User Name"];
                password = vaultConfig[vaultURL]["Password"];

                ScriptEngine engine = Python.CreateEngine();
                ScriptScope scope = engine.CreateScope();
                try
                {
                    ScriptSource script = engine.CreateScriptSourceFromFile(@"buildCmpLib.py");

                    //var paths = engine.GetSearchPaths();
                    //string dir = @"C:\Program Files (x86)\IronPython 2.7\Lib\";
                    //paths.Add(dir);
                    //engine.SetSearchPaths(paths);

                    scope.SetVariable("crPath", crPath);
                    scope.SetVariable("cmpLibPath", cmpLibPath);
                    scope.SetVariable("crType", crType);
                    scope.SetVariable("vaultAddress", vaultURL);
                    scope.SetVariable("userName", userName);
                    scope.SetVariable("pwd", password);
                  
                    var scriptResult = script.Execute(scope);
                    MessageBox.Show("Cmplib Built");                   
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message);
                }
                
           
        }

        public void loginVault(string vaultURL, string userName, string password)
        {
            IDSClient idsClient = new IDSClient(vaultURL + "/ids/?cls=soap");
            try
            {
                IDSLoginResult loginResult = idsClient.Login(userName, password, false);
                vaultClient = new VaultClient(vaultURL + "/vault/?cls=soap");
                vaultClient.Login(loginResult.SessionId);           
              
            }

            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
               
            }

        }

        private void btnOpenCR_Click(object sender, EventArgs e)
        {
            OpenFileDialog dlg = new OpenFileDialog();
            dlg.Multiselect = false;
            dlg.InitialDirectory = this.txtCR.Text;
            dlg.Filter = "csv|*.csv";
            dlg.FilterIndex = 1;

            if (dlg.ShowDialog() == DialogResult.OK)
            {
                this.txtCR.Text = dlg.FileName;
            }
        }

        private void btnOpenCmp_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog dlg = new FolderBrowserDialog();
            if(dlg.ShowDialog() == DialogResult.OK)
            {
                this.txtCMP.Text = dlg.SelectedPath;
            }
        }

        private void btnDefSourceFolder_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog dlg = new FolderBrowserDialog();
            if (dlg.ShowDialog() == DialogResult.OK)
            {
                this.txtSrcFolder.Text = dlg.SelectedPath;
            }
        }

        private void btnDefTarFolder_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog dlg = new FolderBrowserDialog();
            if (dlg.ShowDialog() == DialogResult.OK)
            {
                this.txtTarFolder.Text = dlg.SelectedPath;
            }
        }

        private void mainForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            var parser = new FileIniDataParser();
            IniData config = parser.ReadFile("Config.ini");
            Boolean configFound = false;
            foreach (SectionData section in config.Sections)
            {
                if (section.SectionName == "Release Config") configFound = true;
            }

            if(!configFound)
            {
                config.Sections.AddSection("Release Config");
                config["Release Config"].AddKey("CmpLib File", this.txtCMP.Text);
                config["Release Config"].AddKey("Component Record", this.txtCR.Text);
                config["Release Config"].AddKey("Source Folder", this.txtSrcFolder.Text);
                config["Release Config"].AddKey("Target Folder", this.txtTarFolder.Text);
            }
            else
            {
                config["Release Config"]["CmpLib File"] = this.txtCMP.Text;
                config["Release Config"]["Component Record"] = this.txtCR.Text;
                config["Release Config"]["Source Folder"] = this.txtSrcFolder.Text;
                config["Release Config"]["Target Folder"] = this.txtTarFolder.Text;
            }

            parser.WriteFile("Config.ini", config);
        }
    }
}
