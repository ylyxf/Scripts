namespace ApiClient
{
    partial class SelectApiKey
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
            this.tbUsername = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.lsApiKey = new System.Windows.Forms.ListView();
            this.colApiKey = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.colBalance = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.colFreeBalance = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.colExpireDate = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.btSearch = new System.Windows.Forms.Button();
            this.btOK = new System.Windows.Forms.Button();
            this.btCancel = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // tbUsername
            // 
            this.tbUsername.Location = new System.Drawing.Point(80, 12);
            this.tbUsername.Name = "tbUsername";
            this.tbUsername.Size = new System.Drawing.Size(200, 20);
            this.tbUsername.TabIndex = 1;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(12, 15);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(55, 13);
            this.label6.TabIndex = 2;
            this.label6.Text = "Username";
            // 
            // lsApiKey
            // 
            this.lsApiKey.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.colApiKey,
            this.colBalance,
            this.colFreeBalance,
            this.colExpireDate});
            this.lsApiKey.FullRowSelect = true;
            this.lsApiKey.HideSelection = false;
            this.lsApiKey.Location = new System.Drawing.Point(12, 57);
            this.lsApiKey.MultiSelect = false;
            this.lsApiKey.Name = "lsApiKey";
            this.lsApiKey.Size = new System.Drawing.Size(517, 136);
            this.lsApiKey.TabIndex = 3;
            this.lsApiKey.UseCompatibleStateImageBehavior = false;
            this.lsApiKey.View = System.Windows.Forms.View.Details;
            this.lsApiKey.MouseDoubleClick += new System.Windows.Forms.MouseEventHandler(this.lsApiKey_MouseDoubleClick);
            // 
            // colApiKey
            // 
            this.colApiKey.Text = "API Key";
            this.colApiKey.Width = 230;
            // 
            // colBalance
            // 
            this.colBalance.Text = "Balance";
            this.colBalance.Width = 70;
            // 
            // colFreeBalance
            // 
            this.colFreeBalance.Text = "Free";
            this.colFreeBalance.Width = 70;
            // 
            // colExpireDate
            // 
            this.colExpireDate.Text = "Expire Date";
            this.colExpireDate.Width = 140;
            // 
            // btSearch
            // 
            this.btSearch.Location = new System.Drawing.Point(286, 10);
            this.btSearch.Name = "btSearch";
            this.btSearch.Size = new System.Drawing.Size(63, 23);
            this.btSearch.TabIndex = 2;
            this.btSearch.Text = "Search";
            this.btSearch.UseVisualStyleBackColor = true;
            this.btSearch.Click += new System.EventHandler(this.btSearch_Click);
            // 
            // btOK
            // 
            this.btOK.Location = new System.Drawing.Point(397, 206);
            this.btOK.Name = "btOK";
            this.btOK.Size = new System.Drawing.Size(63, 23);
            this.btOK.TabIndex = 4;
            this.btOK.Text = "OK";
            this.btOK.UseVisualStyleBackColor = true;
            this.btOK.Click += new System.EventHandler(this.btOK_Click);
            // 
            // btCancel
            // 
            this.btCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.btCancel.Location = new System.Drawing.Point(466, 206);
            this.btCancel.Name = "btCancel";
            this.btCancel.Size = new System.Drawing.Size(63, 23);
            this.btCancel.TabIndex = 5;
            this.btCancel.Text = "Cancel";
            this.btCancel.UseVisualStyleBackColor = true;
            this.btCancel.Click += new System.EventHandler(this.btCancel_Click);
            // 
            // SelectApiKey
            // 
            this.AcceptButton = this.btOK;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.btCancel;
            this.ClientSize = new System.Drawing.Size(541, 241);
            this.Controls.Add(this.btCancel);
            this.Controls.Add(this.btOK);
            this.Controls.Add(this.btSearch);
            this.Controls.Add(this.lsApiKey);
            this.Controls.Add(this.tbUsername);
            this.Controls.Add(this.label6);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Name = "SelectApiKey";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Search API Key";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox tbUsername;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.ListView lsApiKey;
        private System.Windows.Forms.ColumnHeader colApiKey;
        private System.Windows.Forms.ColumnHeader colBalance;
        private System.Windows.Forms.ColumnHeader colFreeBalance;
        private System.Windows.Forms.ColumnHeader colExpireDate;
        private System.Windows.Forms.Button btSearch;
        private System.Windows.Forms.Button btOK;
        private System.Windows.Forms.Button btCancel;
    }
}