namespace ApiClient
{
    partial class NewApiKey
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
            this.label1 = new System.Windows.Forms.Label();
            this.tbApiKey = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.pickerStartDate = new System.Windows.Forms.DateTimePicker();
            this.label3 = new System.Windows.Forms.Label();
            this.pickerExpiredDate = new System.Windows.Forms.DateTimePicker();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.btCreate = new System.Windows.Forms.Button();
            this.btClose = new System.Windows.Forms.Button();
            this.btGenerate = new System.Windows.Forms.Button();
            this.tbPaidBalance = new System.Windows.Forms.TextBox();
            this.tbFreeBalance = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.tbUsername = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(14, 38);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(45, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "API Key";
            // 
            // tbApiKey
            // 
            this.tbApiKey.Location = new System.Drawing.Point(91, 35);
            this.tbApiKey.Name = "tbApiKey";
            this.tbApiKey.Size = new System.Drawing.Size(240, 20);
            this.tbApiKey.TabIndex = 2;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(14, 66);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(55, 13);
            this.label2.TabIndex = 2;
            this.label2.Text = "Start Date";
            // 
            // pickerStartDate
            // 
            this.pickerStartDate.Location = new System.Drawing.Point(91, 62);
            this.pickerStartDate.Name = "pickerStartDate";
            this.pickerStartDate.Size = new System.Drawing.Size(200, 20);
            this.pickerStartDate.TabIndex = 4;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(14, 93);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(71, 13);
            this.label3.TabIndex = 2;
            this.label3.Text = "Expired Date:";
            // 
            // pickerExpiredDate
            // 
            this.pickerExpiredDate.Location = new System.Drawing.Point(91, 89);
            this.pickerExpiredDate.Name = "pickerExpiredDate";
            this.pickerExpiredDate.Size = new System.Drawing.Size(200, 20);
            this.pickerExpiredDate.TabIndex = 5;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(14, 119);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(70, 13);
            this.label4.TabIndex = 5;
            this.label4.Text = "Paid Balance";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(14, 145);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(70, 13);
            this.label5.TabIndex = 5;
            this.label5.Text = "Free Balance";
            // 
            // btCreate
            // 
            this.btCreate.Location = new System.Drawing.Point(91, 178);
            this.btCreate.Name = "btCreate";
            this.btCreate.Size = new System.Drawing.Size(75, 23);
            this.btCreate.TabIndex = 9;
            this.btCreate.Text = "Create";
            this.btCreate.UseVisualStyleBackColor = true;
            this.btCreate.Click += new System.EventHandler(this.btCreate_Click);
            // 
            // btClose
            // 
            this.btClose.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.btClose.Location = new System.Drawing.Point(172, 178);
            this.btClose.Name = "btClose";
            this.btClose.Size = new System.Drawing.Size(75, 23);
            this.btClose.TabIndex = 10;
            this.btClose.Text = "Close";
            this.btClose.UseVisualStyleBackColor = true;
            this.btClose.Click += new System.EventHandler(this.btClose_Click);
            // 
            // btGenerate
            // 
            this.btGenerate.Location = new System.Drawing.Point(337, 33);
            this.btGenerate.Name = "btGenerate";
            this.btGenerate.Size = new System.Drawing.Size(75, 23);
            this.btGenerate.TabIndex = 3;
            this.btGenerate.Text = "Generate";
            this.btGenerate.UseVisualStyleBackColor = true;
            this.btGenerate.Click += new System.EventHandler(this.btGenerate_Click);
            // 
            // tbPaidBalance
            // 
            this.tbPaidBalance.Location = new System.Drawing.Point(91, 116);
            this.tbPaidBalance.Name = "tbPaidBalance";
            this.tbPaidBalance.Size = new System.Drawing.Size(100, 20);
            this.tbPaidBalance.TabIndex = 6;
            this.tbPaidBalance.Text = "1000";
            // 
            // tbFreeBalance
            // 
            this.tbFreeBalance.Location = new System.Drawing.Point(91, 142);
            this.tbFreeBalance.Name = "tbFreeBalance";
            this.tbFreeBalance.Size = new System.Drawing.Size(100, 20);
            this.tbFreeBalance.TabIndex = 8;
            this.tbFreeBalance.Text = "100";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(14, 13);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(55, 13);
            this.label6.TabIndex = 0;
            this.label6.Text = "Username";
            // 
            // tbUsername
            // 
            this.tbUsername.Location = new System.Drawing.Point(91, 10);
            this.tbUsername.Name = "tbUsername";
            this.tbUsername.Size = new System.Drawing.Size(200, 20);
            this.tbUsername.TabIndex = 1;
            // 
            // NewApiKey
            // 
            this.AcceptButton = this.btCreate;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.btClose;
            this.ClientSize = new System.Drawing.Size(446, 218);
            this.Controls.Add(this.tbFreeBalance);
            this.Controls.Add(this.tbPaidBalance);
            this.Controls.Add(this.btGenerate);
            this.Controls.Add(this.btClose);
            this.Controls.Add(this.btCreate);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.pickerExpiredDate);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.pickerStartDate);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.tbUsername);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.tbApiKey);
            this.Controls.Add(this.label1);
            this.Name = "NewApiKey";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "New API Key";
            this.Load += new System.EventHandler(this.NewApiKey_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox tbApiKey;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.DateTimePicker pickerStartDate;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.DateTimePicker pickerExpiredDate;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Button btCreate;
        private System.Windows.Forms.Button btClose;
        private System.Windows.Forms.Button btGenerate;
        private System.Windows.Forms.TextBox tbPaidBalance;
        private System.Windows.Forms.TextBox tbFreeBalance;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox tbUsername;
    }
}