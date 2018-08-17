using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using IniParser;
using IniParser.Model;
using Altium.Sdk.DxpAppServer;
using Altium.Sdk.DxpAppServer.IDSServiceProxy;

namespace Vault_Release_Tool
{
    public partial class Add_Vault : Form
    {
        private mainForm main_form;
        public Add_Vault(mainForm form)
        {
            InitializeComponent();
            main_form = form;
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            string vaultURL = this.txtBox.Text;
            string userName = this.txtBoxUserName.Text;
            string password = this.txtBoxPW.Text;

            var parser = new FileIniDataParser();
            IniData config = parser.ReadFile("Config.ini");
            if (!config.Configuration.SectionRegex.Equals(vaultURL))
            {
                try
                {
                    if (vaultURL != "")
                    {
                        string loginURL;
                        if (vaultURL == "http://vault.live.altium.com")
                        {
                            loginURL = "http://ids.live.altium.com/?cls=soap";
                            
                        }
                        else
                        {
                            loginURL = vaultURL + "/ids/?cls=soap";
                        }

                        IDSClient idsClient = new IDSClient(loginURL);
                        IDSLoginResult loginReuslt = idsClient.Login(userName, password, false, LoginOptions.KillExistingSession);

                        if (loginReuslt.SessionId != null)
                        {
                            config.Sections.AddSection(vaultURL);
                            config[vaultURL].AddKey("User Name", userName);
                            config[vaultURL].AddKey("Password", password);
                            parser.WriteFile("Config.ini", config);

                            main_form.addVaultToList(vaultURL);

                            this.Close();
                        }
                    }
                }

                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message);

                }
            }

        }
    }
}
