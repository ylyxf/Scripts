namespace ApiClient
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.btLocal = new System.Windows.Forms.Button();
            this.btUat = new System.Windows.Forms.Button();
            this.btDev = new System.Windows.Forms.Button();
            this.btProd = new System.Windows.Forms.Button();
            this.tbPrincipalServer = new System.Windows.Forms.TextBox();
            this.label7 = new System.Windows.Forms.Label();
            this.tbApiServer = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.splitContainer2 = new System.Windows.Forms.SplitContainer();
            this.splitContainer3 = new System.Windows.Forms.SplitContainer();
            this.tabMethod = new System.Windows.Forms.TabControl();
            this.tabApi = new System.Windows.Forms.TabPage();
            this.lsApiMethod = new System.Windows.Forms.ListBox();
            this.panel2 = new System.Windows.Forms.Panel();
            this.btSelectApiKey = new System.Windows.Forms.Button();
            this.btNewKey = new System.Windows.Forms.Button();
            this.tbApiKey = new System.Windows.Forms.TextBox();
            this.tbPassword = new System.Windows.Forms.TextBox();
            this.lbUsernameLegend = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.tabAdmin = new System.Windows.Forms.TabPage();
            this.lsAdminMethod = new System.Windows.Forms.ListBox();
            this.gridParameter = new System.Windows.Forms.PropertyGrid();
            this.panel1 = new System.Windows.Forms.Panel();
            this.lsRequestMethod = new System.Windows.Forms.ComboBox();
            this.btInvoke = new System.Windows.Forms.Button();
            this.label9 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.tbResponse = new EPocalipse.Json.Viewer.JsonViewer();
            this.label6 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).BeginInit();
            this.splitContainer1.Panel1.SuspendLayout();
            this.splitContainer1.Panel2.SuspendLayout();
            this.splitContainer1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer2)).BeginInit();
            this.splitContainer2.Panel1.SuspendLayout();
            this.splitContainer2.Panel2.SuspendLayout();
            this.splitContainer2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer3)).BeginInit();
            this.splitContainer3.Panel1.SuspendLayout();
            this.splitContainer3.Panel2.SuspendLayout();
            this.splitContainer3.SuspendLayout();
            this.tabMethod.SuspendLayout();
            this.tabApi.SuspendLayout();
            this.panel2.SuspendLayout();
            this.tabAdmin.SuspendLayout();
            this.panel1.SuspendLayout();
            this.SuspendLayout();
            // 
            // splitContainer1
            // 
            this.splitContainer1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer1.FixedPanel = System.Windows.Forms.FixedPanel.Panel1;
            this.splitContainer1.IsSplitterFixed = true;
            this.splitContainer1.Location = new System.Drawing.Point(10, 10);
            this.splitContainer1.Name = "splitContainer1";
            this.splitContainer1.Orientation = System.Windows.Forms.Orientation.Horizontal;
            // 
            // splitContainer1.Panel1
            // 
            this.splitContainer1.Panel1.Controls.Add(this.btLocal);
            this.splitContainer1.Panel1.Controls.Add(this.btUat);
            this.splitContainer1.Panel1.Controls.Add(this.btDev);
            this.splitContainer1.Panel1.Controls.Add(this.btProd);
            this.splitContainer1.Panel1.Controls.Add(this.tbPrincipalServer);
            this.splitContainer1.Panel1.Controls.Add(this.label7);
            this.splitContainer1.Panel1.Controls.Add(this.tbApiServer);
            this.splitContainer1.Panel1.Controls.Add(this.label3);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.splitContainer2);
            this.splitContainer1.Size = new System.Drawing.Size(930, 666);
            this.splitContainer1.SplitterDistance = 60;
            this.splitContainer1.TabIndex = 0;
            // 
            // btLocal
            // 
            this.btLocal.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.btLocal.Location = new System.Drawing.Point(879, 0);
            this.btLocal.Name = "btLocal";
            this.btLocal.Size = new System.Drawing.Size(49, 23);
            this.btLocal.TabIndex = 3;
            this.btLocal.Text = "Local";
            this.btLocal.UseVisualStyleBackColor = true;
            this.btLocal.Click += new System.EventHandler(this.btLocal_Click);
            // 
            // btUat
            // 
            this.btUat.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.btUat.Location = new System.Drawing.Point(769, 27);
            this.btUat.Name = "btUat";
            this.btUat.Size = new System.Drawing.Size(49, 23);
            this.btUat.TabIndex = 3;
            this.btUat.Text = "UAT";
            this.btUat.UseVisualStyleBackColor = true;
            this.btUat.Click += new System.EventHandler(this.btUat_Click);
            // 
            // btDev
            // 
            this.btDev.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.btDev.Location = new System.Drawing.Point(824, 1);
            this.btDev.Name = "btDev";
            this.btDev.Size = new System.Drawing.Size(49, 23);
            this.btDev.TabIndex = 3;
            this.btDev.Text = "DEV";
            this.btDev.UseVisualStyleBackColor = true;
            this.btDev.Click += new System.EventHandler(this.btDev_Click);
            // 
            // btProd
            // 
            this.btProd.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.btProd.Location = new System.Drawing.Point(769, 1);
            this.btProd.Name = "btProd";
            this.btProd.Size = new System.Drawing.Size(49, 23);
            this.btProd.TabIndex = 3;
            this.btProd.Text = "PROD";
            this.btProd.UseVisualStyleBackColor = true;
            this.btProd.Click += new System.EventHandler(this.btProd_Click);
            // 
            // tbPrincipalServer
            // 
            this.tbPrincipalServer.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.tbPrincipalServer.Location = new System.Drawing.Point(93, 3);
            this.tbPrincipalServer.Name = "tbPrincipalServer";
            this.tbPrincipalServer.Size = new System.Drawing.Size(670, 20);
            this.tbPrincipalServer.TabIndex = 1;
            this.tbPrincipalServer.Text = "https://94.23.156.95:9043/PrincipalServer/api";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(3, 6);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(84, 13);
            this.label7.TabIndex = 0;
            this.label7.Text = "Principal Server:";
            // 
            // tbApiServer
            // 
            this.tbApiServer.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.tbApiServer.Location = new System.Drawing.Point(93, 29);
            this.tbApiServer.Name = "tbApiServer";
            this.tbApiServer.Size = new System.Drawing.Size(670, 20);
            this.tbApiServer.TabIndex = 2;
            this.tbApiServer.Text = "https://94.23.156.95:9043/ApiServer/api";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(28, 32);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(59, 13);
            this.label3.TabIndex = 0;
            this.label3.Text = "Api Server:";
            // 
            // splitContainer2
            // 
            this.splitContainer2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer2.Location = new System.Drawing.Point(0, 0);
            this.splitContainer2.Name = "splitContainer2";
            this.splitContainer2.Orientation = System.Windows.Forms.Orientation.Horizontal;
            // 
            // splitContainer2.Panel1
            // 
            this.splitContainer2.Panel1.Controls.Add(this.splitContainer3);
            // 
            // splitContainer2.Panel2
            // 
            this.splitContainer2.Panel2.Controls.Add(this.tbResponse);
            this.splitContainer2.Panel2.Controls.Add(this.label6);
            this.splitContainer2.Panel2.Padding = new System.Windows.Forms.Padding(0, 5, 0, 0);
            this.splitContainer2.Size = new System.Drawing.Size(930, 602);
            this.splitContainer2.SplitterDistance = 350;
            this.splitContainer2.TabIndex = 1;
            // 
            // splitContainer3
            // 
            this.splitContainer3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer3.Location = new System.Drawing.Point(0, 0);
            this.splitContainer3.Name = "splitContainer3";
            // 
            // splitContainer3.Panel1
            // 
            this.splitContainer3.Panel1.Controls.Add(this.tabMethod);
            // 
            // splitContainer3.Panel2
            // 
            this.splitContainer3.Panel2.Controls.Add(this.gridParameter);
            this.splitContainer3.Panel2.Controls.Add(this.panel1);
            this.splitContainer3.Panel2.Controls.Add(this.label2);
            this.splitContainer3.Size = new System.Drawing.Size(930, 350);
            this.splitContainer3.SplitterDistance = 550;
            this.splitContainer3.TabIndex = 0;
            // 
            // tabMethod
            // 
            this.tabMethod.Controls.Add(this.tabApi);
            this.tabMethod.Controls.Add(this.tabAdmin);
            this.tabMethod.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tabMethod.Location = new System.Drawing.Point(0, 0);
            this.tabMethod.Name = "tabMethod";
            this.tabMethod.SelectedIndex = 0;
            this.tabMethod.Size = new System.Drawing.Size(550, 350);
            this.tabMethod.TabIndex = 0;
            this.tabMethod.Selected += new System.Windows.Forms.TabControlEventHandler(this.tabMethod_Selected);
            // 
            // tabApi
            // 
            this.tabApi.Controls.Add(this.lsApiMethod);
            this.tabApi.Controls.Add(this.panel2);
            this.tabApi.Location = new System.Drawing.Point(4, 22);
            this.tabApi.Name = "tabApi";
            this.tabApi.Padding = new System.Windows.Forms.Padding(3);
            this.tabApi.Size = new System.Drawing.Size(542, 324);
            this.tabApi.TabIndex = 0;
            this.tabApi.Text = "API Client";
            this.tabApi.UseVisualStyleBackColor = true;
            // 
            // lsApiMethod
            // 
            this.lsApiMethod.Dock = System.Windows.Forms.DockStyle.Fill;
            this.lsApiMethod.FormattingEnabled = true;
            this.lsApiMethod.Location = new System.Drawing.Point(3, 94);
            this.lsApiMethod.Name = "lsApiMethod";
            this.lsApiMethod.Size = new System.Drawing.Size(536, 227);
            this.lsApiMethod.TabIndex = 8;
            this.lsApiMethod.SelectedValueChanged += new System.EventHandler(this.lsApiMethod_SelectedValueChanged);
            // 
            // panel2
            // 
            this.panel2.Controls.Add(this.btSelectApiKey);
            this.panel2.Controls.Add(this.btNewKey);
            this.panel2.Controls.Add(this.tbApiKey);
            this.panel2.Controls.Add(this.tbPassword);
            this.panel2.Controls.Add(this.lbUsernameLegend);
            this.panel2.Controls.Add(this.label4);
            this.panel2.Controls.Add(this.label5);
            this.panel2.Dock = System.Windows.Forms.DockStyle.Top;
            this.panel2.Location = new System.Drawing.Point(3, 3);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(536, 91);
            this.panel2.TabIndex = 0;
            // 
            // btSelectApiKey
            // 
            this.btSelectApiKey.Location = new System.Drawing.Point(414, 23);
            this.btSelectApiKey.Name = "btSelectApiKey";
            this.btSelectApiKey.Size = new System.Drawing.Size(31, 23);
            this.btSelectApiKey.TabIndex = 4;
            this.btSelectApiKey.Text = "...";
            this.btSelectApiKey.UseVisualStyleBackColor = true;
            this.btSelectApiKey.Click += new System.EventHandler(this.btSelectApiKey_Click);
            // 
            // btNewKey
            // 
            this.btNewKey.Location = new System.Drawing.Point(451, 23);
            this.btNewKey.Name = "btNewKey";
            this.btNewKey.Size = new System.Drawing.Size(74, 23);
            this.btNewKey.TabIndex = 4;
            this.btNewKey.Text = "New Key...";
            this.btNewKey.UseVisualStyleBackColor = true;
            this.btNewKey.Click += new System.EventHandler(this.btNewKey_Click);
            // 
            // tbApiKey
            // 
            this.tbApiKey.Location = new System.Drawing.Point(75, 25);
            this.tbApiKey.Name = "tbApiKey";
            this.tbApiKey.Size = new System.Drawing.Size(333, 20);
            this.tbApiKey.TabIndex = 3;
            // 
            // tbPassword
            // 
            this.tbPassword.Location = new System.Drawing.Point(75, 51);
            this.tbPassword.Name = "tbPassword";
            this.tbPassword.Size = new System.Drawing.Size(333, 20);
            this.tbPassword.TabIndex = 5;
            this.tbPassword.UseSystemPasswordChar = true;
            // 
            // lbUsernameLegend
            // 
            this.lbUsernameLegend.AutoSize = true;
            this.lbUsernameLegend.Location = new System.Drawing.Point(72, 9);
            this.lbUsernameLegend.Name = "lbUsernameLegend";
            this.lbUsernameLegend.Size = new System.Drawing.Size(337, 13);
            this.lbUsernameLegend.TabIndex = 0;
            this.lbUsernameLegend.Text = "Use Username or API Key to login depending on the selected method.";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(11, 28);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(58, 13);
            this.label4.TabIndex = 0;
            this.label4.Text = "Username:";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(11, 54);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(56, 13);
            this.label5.TabIndex = 0;
            this.label5.Text = "Password:";
            // 
            // tabAdmin
            // 
            this.tabAdmin.Controls.Add(this.lsAdminMethod);
            this.tabAdmin.Location = new System.Drawing.Point(4, 22);
            this.tabAdmin.Name = "tabAdmin";
            this.tabAdmin.Padding = new System.Windows.Forms.Padding(3);
            this.tabAdmin.Size = new System.Drawing.Size(542, 324);
            this.tabAdmin.TabIndex = 1;
            this.tabAdmin.Text = "Administration";
            this.tabAdmin.UseVisualStyleBackColor = true;
            // 
            // lsAdminMethod
            // 
            this.lsAdminMethod.Dock = System.Windows.Forms.DockStyle.Fill;
            this.lsAdminMethod.FormattingEnabled = true;
            this.lsAdminMethod.Location = new System.Drawing.Point(3, 3);
            this.lsAdminMethod.Name = "lsAdminMethod";
            this.lsAdminMethod.Size = new System.Drawing.Size(536, 318);
            this.lsAdminMethod.TabIndex = 8;
            this.lsAdminMethod.SelectedValueChanged += new System.EventHandler(this.lsAdminMethod_SelectedValueChanged);
            // 
            // gridParameter
            // 
            this.gridParameter.Dock = System.Windows.Forms.DockStyle.Fill;
            this.gridParameter.Location = new System.Drawing.Point(0, 13);
            this.gridParameter.Name = "gridParameter";
            this.gridParameter.Size = new System.Drawing.Size(376, 301);
            this.gridParameter.TabIndex = 7;
            // 
            // panel1
            // 
            this.panel1.Controls.Add(this.lsRequestMethod);
            this.panel1.Controls.Add(this.btInvoke);
            this.panel1.Controls.Add(this.label9);
            this.panel1.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.panel1.Location = new System.Drawing.Point(0, 314);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(376, 36);
            this.panel1.TabIndex = 5;
            // 
            // lsRequestMethod
            // 
            this.lsRequestMethod.FormattingEnabled = true;
            this.lsRequestMethod.Items.AddRange(new object[] {
            "Get",
            "Post",
            "Put",
            "Delete"});
            this.lsRequestMethod.Location = new System.Drawing.Point(59, 12);
            this.lsRequestMethod.Name = "lsRequestMethod";
            this.lsRequestMethod.Size = new System.Drawing.Size(121, 21);
            this.lsRequestMethod.TabIndex = 9;
            // 
            // btInvoke
            // 
            this.btInvoke.Location = new System.Drawing.Point(213, 10);
            this.btInvoke.Name = "btInvoke";
            this.btInvoke.Size = new System.Drawing.Size(92, 23);
            this.btInvoke.TabIndex = 8;
            this.btInvoke.Text = "Invoke";
            this.btInvoke.UseVisualStyleBackColor = true;
            this.btInvoke.Click += new System.EventHandler(this.btInvoke_Click);
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(7, 15);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(46, 13);
            this.label9.TabIndex = 0;
            this.label9.Text = "Method:";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Dock = System.Windows.Forms.DockStyle.Top;
            this.label2.Location = new System.Drawing.Point(0, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(63, 13);
            this.label2.TabIndex = 0;
            this.label2.Text = "Parameters:";
            // 
            // tbResponse
            // 
            this.tbResponse.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tbResponse.Json = "";
            this.tbResponse.Location = new System.Drawing.Point(0, 18);
            this.tbResponse.Name = "tbResponse";
            this.tbResponse.Size = new System.Drawing.Size(930, 230);
            this.tbResponse.TabIndex = 1;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Dock = System.Windows.Forms.DockStyle.Top;
            this.label6.Location = new System.Drawing.Point(0, 5);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(58, 13);
            this.label6.TabIndex = 0;
            this.label6.Text = "Response:";
            // 
            // MainForm
            // 
            this.AcceptButton = this.btInvoke;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(950, 686);
            this.Controls.Add(this.splitContainer1);
            this.Name = "MainForm";
            this.Padding = new System.Windows.Forms.Padding(10);
            this.Text = "MainForm";
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.splitContainer1.Panel1.ResumeLayout(false);
            this.splitContainer1.Panel1.PerformLayout();
            this.splitContainer1.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).EndInit();
            this.splitContainer1.ResumeLayout(false);
            this.splitContainer2.Panel1.ResumeLayout(false);
            this.splitContainer2.Panel2.ResumeLayout(false);
            this.splitContainer2.Panel2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer2)).EndInit();
            this.splitContainer2.ResumeLayout(false);
            this.splitContainer3.Panel1.ResumeLayout(false);
            this.splitContainer3.Panel2.ResumeLayout(false);
            this.splitContainer3.Panel2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer3)).EndInit();
            this.splitContainer3.ResumeLayout(false);
            this.tabMethod.ResumeLayout(false);
            this.tabApi.ResumeLayout(false);
            this.panel2.ResumeLayout(false);
            this.panel2.PerformLayout();
            this.tabAdmin.ResumeLayout(false);
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.SplitContainer splitContainer1;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox tbApiKey;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox tbApiServer;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.SplitContainer splitContainer2;
        private System.Windows.Forms.SplitContainer splitContainer3;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.PropertyGrid gridParameter;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Button btInvoke;
        private System.Windows.Forms.TextBox tbPrincipalServer;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Button btNewKey;
        private System.Windows.Forms.TabControl tabMethod;
        private System.Windows.Forms.TabPage tabApi;
        private System.Windows.Forms.TabPage tabAdmin;
        private System.Windows.Forms.ListBox lsAdminMethod;
        private System.Windows.Forms.TextBox tbPassword;
        private System.Windows.Forms.ListBox lsApiMethod;
        private System.Windows.Forms.Panel panel2;
        private EPocalipse.Json.Viewer.JsonViewer tbResponse;
        private System.Windows.Forms.Button btSelectApiKey;
        private System.Windows.Forms.Button btDev;
        private System.Windows.Forms.Button btProd;
        private System.Windows.Forms.Button btLocal;
        private System.Windows.Forms.ComboBox lsRequestMethod;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Button btUat;
        private System.Windows.Forms.Label lbUsernameLegend;

    }
}