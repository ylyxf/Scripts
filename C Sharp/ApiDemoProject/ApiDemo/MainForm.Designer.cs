namespace ApiDemo
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.lnkCreateApiKey = new System.Windows.Forms.LinkLabel();
            this.lbSubscriptionStatus = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.tbApiKey = new System.Windows.Forms.TextBox();
            this.tbApiServer = new System.Windows.Forms.TextBox();
            this.tbPassword = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.splitContainer2 = new System.Windows.Forms.SplitContainer();
            this.splitContainer3 = new System.Windows.Forms.SplitContainer();
            this.lsApiMethod = new System.Windows.Forms.ListBox();
            this.gridParameter = new System.Windows.Forms.PropertyGrid();
            this.panel1 = new System.Windows.Forms.Panel();
            this.label10 = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.btBacthQuery = new System.Windows.Forms.Button();
            this.btInvoke = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.tbResponse = new EPocalipse.Json.Viewer.JsonViewer();
            this.label6 = new System.Windows.Forms.Label();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
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
            this.splitContainer1.Panel1.Controls.Add(this.lnkCreateApiKey);
            this.splitContainer1.Panel1.Controls.Add(this.lbSubscriptionStatus);
            this.splitContainer1.Panel1.Controls.Add(this.label1);
            this.splitContainer1.Panel1.Controls.Add(this.tbApiKey);
            this.splitContainer1.Panel1.Controls.Add(this.tbApiServer);
            this.splitContainer1.Panel1.Controls.Add(this.tbPassword);
            this.splitContainer1.Panel1.Controls.Add(this.label4);
            this.splitContainer1.Panel1.Controls.Add(this.label3);
            this.splitContainer1.Panel1.Controls.Add(this.label7);
            this.splitContainer1.Panel1.Controls.Add(this.label5);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.splitContainer2);
            this.splitContainer1.Size = new System.Drawing.Size(733, 638);
            this.splitContainer1.SplitterDistance = 100;
            this.splitContainer1.TabIndex = 0;
            // 
            // lnkCreateApiKey
            // 
            this.lnkCreateApiKey.AutoSize = true;
            this.lnkCreateApiKey.Location = new System.Drawing.Point(614, 41);
            this.lnkCreateApiKey.Name = "lnkCreateApiKey";
            this.lnkCreateApiKey.Size = new System.Drawing.Size(70, 13);
            this.lnkCreateApiKey.TabIndex = 7;
            this.lnkCreateApiKey.TabStop = true;
            this.lnkCreateApiKey.Text = "Request One";
            this.lnkCreateApiKey.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.lnkCreateApiKey_LinkClicked);
            // 
            // lbSubscriptionStatus
            // 
            this.lbSubscriptionStatus.AutoSize = true;
            this.lbSubscriptionStatus.Location = new System.Drawing.Point(61, 61);
            this.lbSubscriptionStatus.Name = "lbSubscriptionStatus";
            this.lbSubscriptionStatus.Size = new System.Drawing.Size(99, 13);
            this.lbSubscriptionStatus.TabIndex = 6;
            this.lbSubscriptionStatus.Text = "Subscription Status";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(-1, 87);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(52, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Methods:";
            // 
            // tbApiKey
            // 
            this.tbApiKey.Location = new System.Drawing.Point(64, 38);
            this.tbApiKey.Name = "tbApiKey";
            this.tbApiKey.Size = new System.Drawing.Size(256, 21);
            this.tbApiKey.TabIndex = 3;
            // 
            // tbApiServer
            // 
            this.tbApiServer.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.tbApiServer.Location = new System.Drawing.Point(64, 12);
            this.tbApiServer.Name = "tbApiServer";
            this.tbApiServer.ReadOnly = true;
            this.tbApiServer.Size = new System.Drawing.Size(666, 21);
            this.tbApiServer.TabIndex = 2;
            this.tbApiServer.Text = "https://api.ciiva.com/api";
            // 
            // tbPassword
            // 
            this.tbPassword.Location = new System.Drawing.Point(405, 38);
            this.tbPassword.Name = "tbPassword";
            this.tbPassword.Size = new System.Drawing.Size(160, 21);
            this.tbPassword.TabIndex = 5;
            this.tbPassword.UseSystemPasswordChar = true;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(10, 41);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(49, 13);
            this.label4.TabIndex = 0;
            this.label4.Text = "API Key:";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(-1, 15);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(61, 13);
            this.label3.TabIndex = 0;
            this.label3.Text = "Api Server:";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(571, 41);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(46, 13);
            this.label7.TabIndex = 0;
            this.label7.Text = "No Key?";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(343, 41);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(57, 13);
            this.label5.TabIndex = 0;
            this.label5.Text = "Password:";
            // 
            // splitContainer2
            // 
            this.splitContainer2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer2.FixedPanel = System.Windows.Forms.FixedPanel.Panel1;
            this.splitContainer2.IsSplitterFixed = true;
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
            this.splitContainer2.Size = new System.Drawing.Size(733, 534);
            this.splitContainer2.SplitterDistance = 280;
            this.splitContainer2.TabIndex = 1;
            // 
            // splitContainer3
            // 
            this.splitContainer3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer3.FixedPanel = System.Windows.Forms.FixedPanel.Panel1;
            this.splitContainer3.IsSplitterFixed = true;
            this.splitContainer3.Location = new System.Drawing.Point(0, 0);
            this.splitContainer3.Name = "splitContainer3";
            // 
            // splitContainer3.Panel1
            // 
            this.splitContainer3.Panel1.Controls.Add(this.lsApiMethod);
            // 
            // splitContainer3.Panel2
            // 
            this.splitContainer3.Panel2.Controls.Add(this.gridParameter);
            this.splitContainer3.Panel2.Controls.Add(this.panel1);
            this.splitContainer3.Panel2.Controls.Add(this.label2);
            this.splitContainer3.Size = new System.Drawing.Size(733, 280);
            this.splitContainer3.SplitterDistance = 320;
            this.splitContainer3.TabIndex = 0;
            // 
            // lsApiMethod
            // 
            this.lsApiMethod.Dock = System.Windows.Forms.DockStyle.Fill;
            this.lsApiMethod.FormattingEnabled = true;
            this.lsApiMethod.Location = new System.Drawing.Point(0, 0);
            this.lsApiMethod.Name = "lsApiMethod";
            this.lsApiMethod.Size = new System.Drawing.Size(320, 280);
            this.lsApiMethod.TabIndex = 10;
            this.lsApiMethod.SelectedValueChanged += new System.EventHandler(this.lsApiMethod_SelectedValueChanged);
            // 
            // gridParameter
            // 
            this.gridParameter.Dock = System.Windows.Forms.DockStyle.Fill;
            this.gridParameter.Location = new System.Drawing.Point(0, 13);
            this.gridParameter.Name = "gridParameter";
            this.gridParameter.Size = new System.Drawing.Size(409, 231);
            this.gridParameter.TabIndex = 7;
            // 
            // panel1
            // 
            this.panel1.Controls.Add(this.label10);
            this.panel1.Controls.Add(this.label9);
            this.panel1.Controls.Add(this.label8);
            this.panel1.Controls.Add(this.btBacthQuery);
            this.panel1.Controls.Add(this.btInvoke);
            this.panel1.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.panel1.Location = new System.Drawing.Point(0, 244);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(409, 36);
            this.panel1.TabIndex = 5;
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(294, 15);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(41, 13);
            this.label10.TabIndex = 13;
            this.label10.Text = "label10";
            this.label10.Visible = false;
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(277, 15);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(11, 13);
            this.label9.TabIndex = 12;
            this.label9.Text = "/";
            this.label9.Visible = false;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(236, 15);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(35, 13);
            this.label8.TabIndex = 11;
            this.label8.Text = "label8";
            this.label8.Visible = false;
            // 
            // btBacthQuery
            // 
            this.btBacthQuery.Location = new System.Drawing.Point(118, 10);
            this.btBacthQuery.Name = "btBacthQuery";
            this.btBacthQuery.Size = new System.Drawing.Size(85, 23);
            this.btBacthQuery.TabIndex = 10;
            this.btBacthQuery.Text = "Btach Query";
            this.btBacthQuery.UseVisualStyleBackColor = true;
            this.btBacthQuery.Click += new System.EventHandler(this.btBatchQuery_Click);
            // 
            // btInvoke
            // 
            this.btInvoke.Location = new System.Drawing.Point(3, 10);
            this.btInvoke.Name = "btInvoke";
            this.btInvoke.Size = new System.Drawing.Size(92, 23);
            this.btInvoke.TabIndex = 8;
            this.btInvoke.Text = "Invoke";
            this.btInvoke.UseVisualStyleBackColor = true;
            this.btInvoke.Click += new System.EventHandler(this.btInvoke_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Dock = System.Windows.Forms.DockStyle.Top;
            this.label2.Location = new System.Drawing.Point(0, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(66, 13);
            this.label2.TabIndex = 0;
            this.label2.Text = "Parameters:";
            // 
            // tbResponse
            // 
            this.tbResponse.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tbResponse.Json = "";
            this.tbResponse.Location = new System.Drawing.Point(0, 18);
            this.tbResponse.Name = "tbResponse";
            this.tbResponse.Size = new System.Drawing.Size(733, 232);
            this.tbResponse.TabIndex = 1;
            this.tbResponse.Load += new System.EventHandler(this.tbResponse_Load);
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
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "openFileDialog1";
            // 
            // MainForm
            // 
            this.AcceptButton = this.btInvoke;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(753, 658);
            this.Controls.Add(this.splitContainer1);
            this.Font = new System.Drawing.Font("Tahoma", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "MainForm";
            this.Padding = new System.Windows.Forms.Padding(10);
            this.Text = "Ciiva API Demo";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainForm_FormClosing);
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
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.SplitContainer splitContainer1;
        private System.Windows.Forms.TextBox tbApiServer;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.SplitContainer splitContainer2;
        private System.Windows.Forms.SplitContainer splitContainer3;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.PropertyGrid gridParameter;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Button btInvoke;
        private EPocalipse.Json.Viewer.JsonViewer tbResponse;
        private System.Windows.Forms.ListBox lsApiMethod;
        private System.Windows.Forms.TextBox tbApiKey;
        private System.Windows.Forms.TextBox tbPassword;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label lbSubscriptionStatus;
        private System.Windows.Forms.LinkLabel lnkCreateApiKey;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.Button btBacthQuery;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Label label8;

    }
}