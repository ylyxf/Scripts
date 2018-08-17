using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Ciiva.PrincipalServer.SVS.Dto.ApiSubscription;
using ServiceStack.ServiceClient.Web;

namespace ApiClient
{
    public partial class SelectApiKey : Form
    {
        public SelectApiKey()
        {
            InitializeComponent();
        }

        public Func<string, List<Subscription>> SubscriptionQuerier { get; set; }

        public string SelectedApiKey { get; private set; }

        private void btSearch_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(this.tbUsername.Text))
            {
                MessageBox.Show("Please enter Username.");
                this.tbUsername.SelectAll();
                this.tbUsername.Focus();
                return;
            }

            var subs = this.SubscriptionQuerier(this.tbUsername.Text);
            this.lsApiKey.Items.Clear();
            foreach (var sub in subs)
            {
                ListViewItem item = new ListViewItem();
                item.Text = sub.ApiKey.ToString();
                item.SubItems.AddRange(new string[] { sub.PaidBalance.ToString(), sub.FreeBalance.ToString(), sub.PaidExpireDate.ToString() });
                this.lsApiKey.Items.Add(item);
            }
        }

        private void btOK_Click(object sender, EventArgs e)
        {
            if (this.lsApiKey.SelectedItems.Count == 0)
            {
                MessageBox.Show("Please select an API Key.");
                return;
            }
            this.SelectedApiKey = this.lsApiKey.SelectedItems[0].Text;
            this.DialogResult = System.Windows.Forms.DialogResult.OK;
        }

        private void btCancel_Click(object sender, EventArgs e)
        {
            this.DialogResult = System.Windows.Forms.DialogResult.Cancel;
        }

        private void lsApiKey_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            if (this.lsApiKey.SelectedItems.Count == 0)
                return;
            this.btOK_Click(null, e);
        }
    }
}