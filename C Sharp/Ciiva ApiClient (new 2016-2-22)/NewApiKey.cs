using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ApiClient
{
    public partial class NewApiKey : Form
    {
        public string Username { get; set; }

        public Guid ApiKey { get; set; }

        public DateTime StartDate { get; set; }

        public DateTime ExpiredDate { get; set; }

        public long PaidBalance { get; set; }

        public long FreeBalance { get; set; }

        public NewApiKey()
        {
            InitializeComponent();
        }

        private void NewApiKey_Load(object sender, EventArgs e)
        {
            this.btGenerate_Click(null, null);
            this.pickerExpiredDate.Value = DateTime.Now.AddMonths(1);
            this.tbPaidBalance.Focus();
        }

        private void btGenerate_Click(object sender, EventArgs e)
        {
            this.tbApiKey.Text = Guid.NewGuid().ToString().ToUpper();
        }

        private void btCreate_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(this.tbUsername.Text))
            {
                MessageBox.Show("Please enter Username.");
                this.tbUsername.SelectAll();
                this.tbUsername.Focus();
                return;
            }

            Guid apiKey = Guid.Empty;
            if (!Guid.TryParse(this.tbApiKey.Text, out apiKey))
            {
                MessageBox.Show("Please provide API Key.");
                this.tbApiKey.SelectAll();
                this.tbApiKey.Focus();
                return;
            }

            if (this.pickerStartDate.Value.Date > DateTime.Today)
            {
                MessageBox.Show("Invalid start date.");
                this.pickerStartDate.Focus();
                return;
            }

            if (this.pickerExpiredDate.Value.Date < DateTime.Today || this.pickerExpiredDate.Value.Date < this.pickerStartDate.Value.Date)
            {
                MessageBox.Show("Invalid expired date.");
                this.pickerExpiredDate.Focus();
                return;
            }

            long paidBalance = 0;
            if (!long.TryParse(this.tbPaidBalance.Text, out paidBalance))
            {
                MessageBox.Show("Please enter Paid Balance.");
                this.tbPaidBalance.SelectAll();
                this.tbPaidBalance.Focus();
                return;
            }
            else if (paidBalance < 0)
            {
                MessageBox.Show("Paid Balance cannot be negative.");
                this.tbPaidBalance.SelectAll();
                this.tbPaidBalance.Focus();
                return;
            }

            long freeBalance = 0;
            if (!long.TryParse(this.tbFreeBalance.Text, out freeBalance))
            {
                MessageBox.Show("Please enter Free Balance.");
                this.tbFreeBalance.SelectAll();
                this.tbFreeBalance.Focus();
                return;
            }
            else if (freeBalance < 0)
            {
                MessageBox.Show("Free Balance cannot be negative.");
                this.tbFreeBalance.SelectAll();
                this.tbFreeBalance.Focus();
                return;
            }

            this.Username = tbUsername.Text;

            this.ApiKey = apiKey;
            
            this.StartDate = this.pickerStartDate.Value;
            
            this.ExpiredDate = this.pickerExpiredDate.Value;

            this.PaidBalance = paidBalance;

            this.FreeBalance = freeBalance;

            this.DialogResult = System.Windows.Forms.DialogResult.OK;
        }

        private void btClose_Click(object sender, EventArgs e)
        {
            this.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.Close();
        }
    }
}
