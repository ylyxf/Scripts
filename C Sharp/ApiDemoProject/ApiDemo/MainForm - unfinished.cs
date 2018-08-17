using System;
using System.Threading;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Windows.Forms;
using ServiceStack.Common.ServiceClient.Web;
using ServiceStack.ServiceClient.Web;
using ServiceStack.ServiceHost;
using ServiceStack.Text;
using System.ComponentModel;
using System.Reflection;
using System.Web;
using Ciiva.Api.Dto;
using LumenWorks.Framework.IO.Csv;
using fastJSON;
using NetJSON = Newtonsoft.Json;
using System.Text.RegularExpressions;

namespace ApiDemo
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            // Trust server certificate
            ServicePointManager.ServerCertificateValidationCallback += (sender, cert, chain, sslPolicyErrors) => true;

            InitializeComponent();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            this.LoadUserSettings();

            this.lbSubscriptionStatus.Text = string.Empty;

            this.lsApiMethod.DataSource = typeof(Ciiva.Api.Dto.AuthenticationRequest).Assembly.GetTypes()
                .Where(t => t.Name.StartsWith("Get"))
                .OrderBy(t => t.Name)
                .Select(t => new TypeListItem(t))
                .ToList();

        
        }

        private Dictionary<Type, object> parameters = new Dictionary<Type, object>();

        private void lsApiMethod_SelectedValueChanged(object sender, EventArgs e)
        {
            var selecteditem = this.lsApiMethod.SelectedItem as TypeListItem;
            if (selecteditem == null)
                return;

            var type = selecteditem.Type;
            object parameter = null;
            if (!this.parameters.TryGetValue(type, out parameter))
            {
                parameter = Activator.CreateInstance(type);
                MainForm.SetDefaultPropertyValues(type, parameter);
                this.parameters[type] = parameter;
            }
            this.gridParameter.SelectedObject = parameter;
        }

        private static void SetDefaultPropertyValues(Type type, object parameter)
        {
            type.GetProperties().ToList().ForEach(p =>
            {
                var attrs = p.GetCustomAttributes(typeof(DefaultValueAttribute), false);
                if (attrs.Length == 1)
                {
                    p.SetValue(parameter, ((DefaultValueAttribute)attrs[0]).Value, null);
                }
            });
        }

        private Tuple<string, string> apiWebClientAuth = new Tuple<string, string>(null, null);
        private WebClientEx apiWebClient = null;
        public WebClient GetApiWebClient(string baseUri, string username, string password)
        {
            if (apiWebClient == null || apiWebClient.BaseAddress != baseUri || apiWebClientAuth.Item1 != username || apiWebClientAuth.Item2 != password)
            {
                apiWebClient = null;

                var client = new WebClientEx();
                client.BaseAddress = baseUri;
                
                var auth = new AuthenticationRequest
                {
                    Username = username,
                    Password = password
                };

                try
                {
                    string authResponse = this.ExecuteOnJsonServiceClient(client, auth);
                    apiWebClient = client;
                    apiWebClientAuth = new Tuple<string, string>(username, password);
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.ToString(), "Authentication is failed.");
                }
            }

            return apiWebClient;
        }

        private void btInvoke_Click(object sender, EventArgs e)
        {
            this.tbResponse.Json = string.Empty;

            try
            {
/*                object selectedParameter = this.gridParameter.SelectedObject;
                if (selectedParameter == null)
                {
                    MessageBox.Show("Please select a method to invoke.");
                    this.lsApiMethod.Focus();
                    return;
                }*/

                Guid apiKey = Guid.Empty;
                if (!Guid.TryParse(this.tbApiKey.Text, out apiKey))
                {
                    MessageBox.Show("Please provide API Key.");
                    this.tbApiKey.SelectAll();
                    this.tbApiKey.Focus();
                    return;
                }

                string password = this.tbPassword.Text;
                if (string.IsNullOrWhiteSpace(password))
                {
                    MessageBox.Show("Please enter password.");
                    this.tbPassword.SelectAll();
                    this.tbPassword.Focus();
                    return;
                }

                string serverUrl = this.tbApiServer.Text;
                if (string.IsNullOrWhiteSpace(serverUrl))
                {
                    MessageBox.Show("Please specify API server.");
                    this.tbApiServer.SelectAll();
                    this.tbApiServer.Focus();
                    return;
                }

                
                object selectedParameter = this.gridParameter.SelectedObject;
      
                if (selectedParameter == null)
                {
                    MessageBox.Show("Please select a method to invoke.");
                    this.lsApiMethod.Focus();
                    return;
                }

                WebClient client = this.GetApiWebClient(serverUrl, apiKey.ToString(), password);
                if (client != null)
                {
                    
                    string response = this.ExecuteOnJsonServiceClient(client, selectedParameter);
                    this.tbResponse.Json = response;

                    this.UpdateSubscriptionStatus(client);
                }
            }
            catch (System.Net.WebException ex)
            {
                this.tbResponse.Json = ex.GetResponseBody();
            }
            catch (Exception ex)
            {
                this.tbResponse.Json = ex.ToString();
            }
        }
        
        private string ExecuteOnJsonServiceClient(WebClient client, object dto)
        {
            if (client == null || dto == null)
                throw new ArgumentNullException("Invalid request data.");

            RouteAttribute routeAttr = (RouteAttribute)Attribute.GetCustomAttribute(dto.GetType(), typeof(RouteAttribute));
            string url = client.BaseAddress + routeAttr.Path;

            client.Headers[HttpRequestHeader.ContentType] = "application/x-www-form-urlencoded";

            List<string> parameters = new List<string>();
            foreach (PropertyInfo prop in dto.GetType().GetProperties())
            {
                string parameter = string.Format("{0}={1}", prop.Name, this.JsonSerializeCompoundParameter(prop.GetValue(dto, null)));
                parameters.Add(parameter);
            }

            return client.UploadString(url, string.Join("&", parameters));
        }

        private string JsonSerializeCompoundParameter(object parameterValue)
        {
            if (parameterValue == null)
                return "";
            if (parameterValue is string || parameterValue.GetType().IsValueType)
                return parameterValue.ToString();
            return JsonSerializer.SerializeToString(parameterValue);
        }

        private void UpdateSubscriptionStatus(WebClient client)
        {
            string result = this.ExecuteOnJsonServiceClient(client, new Ciiva.Api.Dto.GetSubscriptionStatus());
            try
            {
                var subscriptionStatus = JsonSerializer.DeserializeFromString<SubscriptionStatus>(result);
                if (subscriptionStatus != null)
                {
                    this.lbSubscriptionStatus.Text = string.Format("Free Credit: {0}     Expire: {1:dd-MMM-yyyy}     Paid Credit: {2}     Expire: {3:dd-MMM-yyyy}",
                        subscriptionStatus.FreeBalance, subscriptionStatus.FreeExpireDate, subscriptionStatus.PaidBalance, subscriptionStatus.PaidExpireDate);
                }
            }
            catch
            {
                this.lbSubscriptionStatus.Text = "[Cannot query subscription status]";
            }
        }

        private void MainForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            this.SaveUserSettings();
        }

        private void LoadUserSettings()
        {
            Guid settingApiKey = Properties.Settings.Default.ApiKey;
            if (settingApiKey != Guid.Empty)
                this.tbApiKey.Text = settingApiKey.ToString();
        }

        private void SaveUserSettings()
        {
            Guid apiKey = Guid.Empty;
            Guid.TryParse(this.tbApiKey.Text, out apiKey);
            Properties.Settings.Default.ApiKey = apiKey;
            
            Properties.Settings.Default.Save();
        }

        private void lnkCreateApiKey_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            // Navigate to a URL.
            System.Diagnostics.Process.Start("https://ciiva.com/api/management");
        }

  

        private void btBatchQuery_Click(object sender, EventArgs e)
        {
           
            openFileDialog1.Filter = "common delimited file(*.csv)|*.csv";
            List<string> results = new List<string>();

            if (openFileDialog1.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                string fi = openFileDialog1.FileName;

                using (CsvReader csv = new CsvReader(new System.IO.StreamReader(fi), true))
                {
                    this.label8.Text = "0";
                    this.label8.Visible = true;

                    int fieldCount = csv.FieldCount;
                    string[] headers = csv.GetFieldHeaders();
                    string res = "";

                    int rowCount = 1;
                    WebClient client = getAuth();
                    while (csv.ReadNextRecord())
                    {
                       res = queryCiiva(csv[0], csv[1],client);
                       if (res != "error")
                       {
                           results.Add(res);
                       }
                       rowCount++;

                       Thread TupdateProgress = new Thread(() => updateProgress(rowCount));
                       TupdateProgress.Start();
           
                    }
                }
            }

            using (System.IO.StreamWriter file = new System.IO.StreamWriter(@"G:\TestArea\ApiDemoProject\JSON.txt"))
            {
                foreach (string line in results)
                {                   
                        file.WriteLine(line);
                }
            }

            MessageBox.Show("Finished");
         }

        delegate void SetValueCallBack(int value);
        public void updateProgress(int value)
        {
            Thread.Sleep(10);
            if (label8.InvokeRequired)
            {
                SetValueCallBack d = new SetValueCallBack(updateProgress);
                this.Invoke(d, new object[] { value });
            }
            else 
            {
                this.label8.Text = value.ToString();
                this.label8.Visible = true;
            }
        }

        private string queryCiiva(string partnumber, string manufacturer, WebClient cli)
        {


                var selectedComponent = new Ciiva.Api.Dto.GetManufacturerComponentsByPartNumber();
                selectedComponent.ManufacturerPartNumber = partnumber;
                selectedComponent.ManufacturerName = manufacturer;
                selectedComponent.Limit = 1;
                selectedComponent.ExactMatch = true;
                selectedComponent.ExtraInfo = true;

                if (selectedComponent == null)
                {
                    MessageBox.Show("Please select a method to invoke.");
                    this.lsApiMethod.Focus();
                    return "error";
                }


                if (cli != null)
                {

                    string response = this.ExecuteOnJsonServiceClient(cli, selectedComponent);
                    Regex reg = new Regex("ManufacturerComponentId\":(.+?),");
                   
                    if (reg.IsMatch(response))
                    {
                        Match match = reg.Match(response);
                        string componentID = match.Groups[1].Value;
                        var selectParam = new Ciiva.Api.Dto.GetManufacturerComponentById();
                        selectParam.ManufacturerComponentId = Convert.ToInt64(componentID);

                        string responseParam = this.ExecuteOnJsonServiceClient(cli, selectParam);
                        return responseParam;
                    }
                    
                    
                    this.UpdateSubscriptionStatus(cli);
                    
                }

                return "error";
        }

        private WebClient getAuth()
        {
            Guid apiKey = Guid.Empty;
            if (!Guid.TryParse(this.tbApiKey.Text, out apiKey))
            {
                MessageBox.Show("Please provide API Key.");
                this.tbApiKey.SelectAll();
                this.tbApiKey.Focus();
                return null;
            }

            string password = this.tbPassword.Text;
            if (string.IsNullOrWhiteSpace(password))
            {
                MessageBox.Show("Please enter password.");
                this.tbPassword.SelectAll();
                this.tbPassword.Focus();
                return null;
            }

            string serverUrl = this.tbApiServer.Text;
            if (string.IsNullOrWhiteSpace(serverUrl))
            {
                MessageBox.Show("Please specify API server.");
                this.tbApiServer.SelectAll();
                this.tbApiServer.Focus();
                return null;
            }

            WebClient client = this.GetApiWebClient(serverUrl, apiKey.ToString(), password);

            return client;
        }

        private void tbResponse_Load(object sender, EventArgs e)
        {

        }

        public static object GetPropertyValue(object info, string field)
        {
            if (info == null) return null;
            Type t = info.GetType();
            IEnumerable<System.Reflection.PropertyInfo> property = from pi in t.GetProperties() where pi.Name.ToLower() == field.ToLower() select pi;
            return property.First().GetValue(info, null);
        }

        public class Component
        {
            public Object Description;
            public string ManufacturerComponentId;
            public Object ManufacturerName;
            public Object ManufacturerNameAlias;
            public Object ManufacturerPartImageURL;
            public Object ManufacturerPartNumber;
            public Object ManufacturerPartURL;
            public Object LifeCycleStatusId;
            public Object LifeCycleStatusName;
            public Object TechnicalDetails;
            public Object LowestPriceBreaks;
            public Object DatasheetURLs;
            public Object Categories;

        }
    }
}