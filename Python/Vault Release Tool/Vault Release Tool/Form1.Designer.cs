namespace Vault_Release_Tool
{
    partial class mainForm
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(mainForm));
            this.label1 = new System.Windows.Forms.Label();
            this.dlVault = new System.Windows.Forms.ComboBox();
            this.btnAddVault = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.txtCR = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.txtCMP = new System.Windows.Forms.TextBox();
            this.txtSrcFolder = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.txtTarFolder = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.rbTI = new System.Windows.Forms.RadioButton();
            this.rbAltium = new System.Windows.Forms.RadioButton();
            this.checkBoxCopy = new System.Windows.Forms.CheckBox();
            this.btnCopy = new System.Windows.Forms.Button();
            this.btnBuild = new System.Windows.Forms.Button();
            this.btnOpenCR = new System.Windows.Forms.Button();
            this.btnOpenCmp = new System.Windows.Forms.Button();
            this.btnDefSourceFolder = new System.Windows.Forms.Button();
            this.btnDefTarFolder = new System.Windows.Forms.Button();
            this.diaOpenCR = new System.Windows.Forms.OpenFileDialog();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(26, 43);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(31, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Vault";
            // 
            // dlVault
            // 
            this.dlVault.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.dlVault.FormattingEnabled = true;
            this.dlVault.Location = new System.Drawing.Point(139, 39);
            this.dlVault.Name = "dlVault";
            this.dlVault.Size = new System.Drawing.Size(195, 21);
            this.dlVault.TabIndex = 2;
            // 
            // btnAddVault
            // 
            this.btnAddVault.Location = new System.Drawing.Point(353, 39);
            this.btnAddVault.Name = "btnAddVault";
            this.btnAddVault.Size = new System.Drawing.Size(77, 21);
            this.btnAddVault.TabIndex = 3;
            this.btnAddVault.Text = "Add Vault";
            this.btnAddVault.UseVisualStyleBackColor = true;
            this.btnAddVault.Click += new System.EventHandler(this.btnAddVault_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(26, 75);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(99, 13);
            this.label2.TabIndex = 4;
            this.label2.Text = "Component Record";
            // 
            // txtCR
            // 
            this.txtCR.Location = new System.Drawing.Point(139, 75);
            this.txtCR.Name = "txtCR";
            this.txtCR.Size = new System.Drawing.Size(195, 20);
            this.txtCR.TabIndex = 5;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(26, 112);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(83, 13);
            this.label3.TabIndex = 6;
            this.label3.Text = "Output Location";
            // 
            // txtCMP
            // 
            this.txtCMP.Location = new System.Drawing.Point(139, 109);
            this.txtCMP.Name = "txtCMP";
            this.txtCMP.Size = new System.Drawing.Size(195, 20);
            this.txtCMP.TabIndex = 7;
            // 
            // txtSrcFolder
            // 
            this.txtSrcFolder.Location = new System.Drawing.Point(139, 141);
            this.txtSrcFolder.Name = "txtSrcFolder";
            this.txtSrcFolder.Size = new System.Drawing.Size(195, 20);
            this.txtSrcFolder.TabIndex = 9;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(26, 144);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(73, 13);
            this.label4.TabIndex = 8;
            this.label4.Text = "Source Folder";
            // 
            // txtTarFolder
            // 
            this.txtTarFolder.Location = new System.Drawing.Point(139, 176);
            this.txtTarFolder.Name = "txtTarFolder";
            this.txtTarFolder.Size = new System.Drawing.Size(195, 20);
            this.txtTarFolder.TabIndex = 11;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(26, 179);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(70, 13);
            this.label5.TabIndex = 10;
            this.label5.Text = "Target Folder";
            // 
            // rbTI
            // 
            this.rbTI.AutoSize = true;
            this.rbTI.Location = new System.Drawing.Point(353, 73);
            this.rbTI.Name = "rbTI";
            this.rbTI.Size = new System.Drawing.Size(73, 17);
            this.rbTI.TabIndex = 12;
            this.rbTI.Text = "TI Record";
            this.rbTI.UseVisualStyleBackColor = true;
            // 
            // rbAltium
            // 
            this.rbAltium.AutoSize = true;
            this.rbAltium.Checked = true;
            this.rbAltium.Location = new System.Drawing.Point(353, 96);
            this.rbAltium.Name = "rbAltium";
            this.rbAltium.Size = new System.Drawing.Size(91, 17);
            this.rbAltium.TabIndex = 13;
            this.rbAltium.TabStop = true;
            this.rbAltium.Text = "Altium Record";
            this.rbAltium.UseVisualStyleBackColor = true;
            // 
            // checkBoxCopy
            // 
            this.checkBoxCopy.AutoSize = true;
            this.checkBoxCopy.Location = new System.Drawing.Point(74, 280);
            this.checkBoxCopy.Name = "checkBoxCopy";
            this.checkBoxCopy.Size = new System.Drawing.Size(156, 17);
            this.checkBoxCopy.TabIndex = 14;
            this.checkBoxCopy.Text = "Don\'t copy released models";
            this.checkBoxCopy.UseVisualStyleBackColor = true;
            // 
            // btnCopy
            // 
            this.btnCopy.Location = new System.Drawing.Point(74, 232);
            this.btnCopy.Name = "btnCopy";
            this.btnCopy.Size = new System.Drawing.Size(96, 33);
            this.btnCopy.TabIndex = 15;
            this.btnCopy.Text = "Copy Models";
            this.btnCopy.UseVisualStyleBackColor = true;
            // 
            // btnBuild
            // 
            this.btnBuild.Location = new System.Drawing.Point(268, 232);
            this.btnBuild.Name = "btnBuild";
            this.btnBuild.Size = new System.Drawing.Size(94, 33);
            this.btnBuild.TabIndex = 16;
            this.btnBuild.Text = "Build CmpLib";
            this.btnBuild.UseVisualStyleBackColor = true;
            this.btnBuild.Click += new System.EventHandler(this.btnBuild_Click);
            // 
            // btnOpenCR
            // 
            this.btnOpenCR.Image = ((System.Drawing.Image)(resources.GetObject("btnOpenCR.Image")));
            this.btnOpenCR.Location = new System.Drawing.Point(313, 75);
            this.btnOpenCR.Name = "btnOpenCR";
            this.btnOpenCR.Size = new System.Drawing.Size(20, 19);
            this.btnOpenCR.TabIndex = 17;
            this.btnOpenCR.UseVisualStyleBackColor = true;
            this.btnOpenCR.Click += new System.EventHandler(this.btnOpenCR_Click);
            // 
            // btnOpenCmp
            // 
            this.btnOpenCmp.Image = ((System.Drawing.Image)(resources.GetObject("btnOpenCmp.Image")));
            this.btnOpenCmp.Location = new System.Drawing.Point(313, 110);
            this.btnOpenCmp.Name = "btnOpenCmp";
            this.btnOpenCmp.Size = new System.Drawing.Size(20, 19);
            this.btnOpenCmp.TabIndex = 18;
            this.btnOpenCmp.UseVisualStyleBackColor = true;
            this.btnOpenCmp.Click += new System.EventHandler(this.btnOpenCmp_Click);
            // 
            // btnDefSourceFolder
            // 
            this.btnDefSourceFolder.Image = ((System.Drawing.Image)(resources.GetObject("btnDefSourceFolder.Image")));
            this.btnDefSourceFolder.Location = new System.Drawing.Point(313, 142);
            this.btnDefSourceFolder.Name = "btnDefSourceFolder";
            this.btnDefSourceFolder.Size = new System.Drawing.Size(20, 19);
            this.btnDefSourceFolder.TabIndex = 19;
            this.btnDefSourceFolder.UseVisualStyleBackColor = true;
            this.btnDefSourceFolder.Click += new System.EventHandler(this.btnDefSourceFolder_Click);
            // 
            // btnDefTarFolder
            // 
            this.btnDefTarFolder.Image = ((System.Drawing.Image)(resources.GetObject("btnDefTarFolder.Image")));
            this.btnDefTarFolder.Location = new System.Drawing.Point(313, 177);
            this.btnDefTarFolder.Name = "btnDefTarFolder";
            this.btnDefTarFolder.Size = new System.Drawing.Size(20, 19);
            this.btnDefTarFolder.TabIndex = 20;
            this.btnDefTarFolder.UseVisualStyleBackColor = true;
            this.btnDefTarFolder.Click += new System.EventHandler(this.btnDefTarFolder_Click);
            // 
            // diaOpenCR
            // 
            this.diaOpenCR.FileName = "openFileDialog1";
            // 
            // mainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(489, 328);
            this.Controls.Add(this.btnDefTarFolder);
            this.Controls.Add(this.btnDefSourceFolder);
            this.Controls.Add(this.btnOpenCmp);
            this.Controls.Add(this.btnOpenCR);
            this.Controls.Add(this.btnBuild);
            this.Controls.Add(this.btnCopy);
            this.Controls.Add(this.checkBoxCopy);
            this.Controls.Add(this.rbAltium);
            this.Controls.Add(this.rbTI);
            this.Controls.Add(this.txtTarFolder);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.txtSrcFolder);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.txtCMP);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.txtCR);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.btnAddVault);
            this.Controls.Add(this.dlVault);
            this.Controls.Add(this.label1);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Location = new System.Drawing.Point(800, 800);
            this.Name = "mainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Release Tool";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.mainForm_FormClosing);
            this.Load += new System.EventHandler(this.mainForm_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox dlVault;
        private System.Windows.Forms.Button btnAddVault;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox txtCR;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox txtCMP;
        private System.Windows.Forms.TextBox txtSrcFolder;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox txtTarFolder;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.RadioButton rbTI;
        private System.Windows.Forms.RadioButton rbAltium;
        private System.Windows.Forms.CheckBox checkBoxCopy;
        private System.Windows.Forms.Button btnCopy;
        private System.Windows.Forms.Button btnBuild;
        private System.Windows.Forms.Button btnOpenCR;
        private System.Windows.Forms.Button btnOpenCmp;
        private System.Windows.Forms.Button btnDefSourceFolder;
        private System.Windows.Forms.Button btnDefTarFolder;
        private System.Windows.Forms.OpenFileDialog diaOpenCR;
    }
}

