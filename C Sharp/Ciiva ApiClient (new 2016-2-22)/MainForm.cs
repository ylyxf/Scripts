using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Net;
using System.Windows.Forms;
using System.Text.RegularExpressions;
using Ciiva.PrincipalServer.SVS.Dto.ApiSubscription;
using ServiceStack.Common.ServiceClient.Web;
using ServiceStack.ServiceClient.Web;
using ServiceStack.ServiceHost;
using ServiceStack.Text;

namespace ApiClient
{
    public partial class MainForm : Form
    {
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

        public MainForm()
        {
            InitializeComponent();

            this.LoadUserSettings();

            // Trust server certificate
            ServicePointManager.ServerCertificateValidationCallback += (sender, cert, chain, sslPolicyErrors) => true;
        }

        private void LoadUserSettings()
        {
            this.tbPrincipalServer.Text = Properties.Settings.Default.PrincipalServer;
            this.tbApiServer.Text = Properties.Settings.Default.ApiServer;
            this.tbApiKey.Text = Properties.Settings.Default.ApiKey;
        }

        private void SaveUserSettings()
        {
            if (!string.IsNullOrWhiteSpace(this.tbPrincipalServer.Text))
                Properties.Settings.Default.PrincipalServer = this.tbPrincipalServer.Text;
            if (!string.IsNullOrWhiteSpace(this.tbApiServer.Text))
                Properties.Settings.Default.ApiServer = this.tbApiServer.Text;
            if (!string.IsNullOrWhiteSpace(this.tbApiKey.Text))
                Properties.Settings.Default.ApiKey = this.tbApiKey.Text;
            Properties.Settings.Default.Save();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            var apiMethods = typeof(Ciiva.ApiServer.SVS.ClientDto.AuthenticationRequest).Assembly.GetTypes()
                .Where(t => t.Name.EndsWith("Request"))
                .Concat(typeof(Ciiva.ApiServer.SVS.AltiumClientDto.SetAltiumIdToCiivaIdRequest).Assembly.GetTypes().Where(t => t.Name.EndsWith("Request")))
                .OrderBy(t => t.FullName)
                .Select(t => new TypeListItem(t))
                .ToList();

            this.lsApiMethod.DataSource = apiMethods;

            this.lsAdminMethod.DataSource = typeof(Ciiva.PrincipalServer.SVS.Dto.InternalAuthInfo).Assembly.GetTypes()
                .Where(t => t.Name.StartsWith("Request"))
                .OrderBy(t => t.FullName)
                .Select(t => new TypeListItem(t))
                .ToList();

            this.lsRequestMethod.SelectedIndex = 1;

#if DEBUG
            this.tbPrincipalServer.Text = "https://localhost/PrincipalServer/api";
            this.tbApiServer.Text = "https://localhost/ApiServer/api";
#endif
        }

        private Dictionary<Type, object> parameters = new Dictionary<Type, object>();

        private void lsApiMethod_SelectedValueChanged(object sender, EventArgs e)
        {
            this.SetPropertyWindows(this.lsApiMethod.SelectedItem as TypeListItem);
        }

        private void lsAdminMethod_SelectedValueChanged(object sender, EventArgs e)
        {
            this.SetPropertyWindows(this.lsAdminMethod.SelectedItem as TypeListItem);
        }

        private void SetPropertyWindows(TypeListItem selectedItem)
        {
            if (selectedItem == null)
                return;

            var type = selectedItem.Type;
            object parameter = null;
            if (!this.parameters.TryGetValue(type, out parameter))
            {
                parameter = Activator.CreateInstance(type);
                MainForm.SetDefaultPropertyValues(type, parameter);
                this.parameters[type] = parameter;
            }
            this.gridParameter.SelectedObject = parameter;
        }

        private JsonServiceClient adminClient = null;

        public JsonServiceClient GetAdminClient(string baseUri)
        {
            if (adminClient == null || adminClient.BaseUri != baseUri)
            {
                adminClient = null;

                var client = new JsonServiceClient(baseUri);
                AuthResponse authResponse = client.Post(new Auth
                {
                    UserName = "EDD8C7D1-0AC8-4AC6-B97E-F842498E8C10",
                    Password = "DED4A798-1EB2-4465-966D-7C39A1876C49",
                    provider = "internal",
                });

                if (authResponse.ResponseStatus.ErrorCode != null)
                    MessageBox.Show(string.Join("\n", authResponse.ResponseStatus.Errors.Select(x => x.Message)), string.Format("Error [{0}]", authResponse.ResponseStatus.ErrorCode));
                else

                    adminClient = client;
            }

            return adminClient;
        }

        private JsonServiceClient apiClient = null;

        public JsonServiceClient GetApiClient(string baseUri, string username, string password)
        {
            if (apiClient == null || apiClient.BaseUri != baseUri || apiClient.UserName != username || apiClient.Password != password)
            {
                apiClient = null;

                string provider = "apikey";
                Guid apiKey;
                if (!Guid.TryParse(username, out apiKey))
                    provider = "ciiva";

                var client = new JsonServiceClient(baseUri);
                AuthResponse authResponse = client.Post(new Auth
                {
                    UserName = username,
                    Password = password,
                    provider = provider,
                });

                if (authResponse.ResponseStatus.ErrorCode != null)
                    MessageBox.Show(string.Join("\n", authResponse.ResponseStatus.Errors.Select(x => x.Message)), string.Format("Error [{0}]", authResponse.ResponseStatus.ErrorCode));
                else
                    apiClient = client;
            }

            return apiClient;
        }

        private void btInvoke_Click(object sender, EventArgs e)
        {
            this.tbResponse.Json = string.Empty;

            var selectedTab = this.tabMethod.SelectedTab;

            try
            {
                object selectedParameter = this.gridParameter.SelectedObject;
                if (selectedParameter == null)
                {
                    MessageBox.Show("Please select a method to invoke.");
                    this.lsApiMethod.Focus();
                    return;
                }

                if (selectedTab == this.tabApi)
                {
                    string username = this.tbApiKey.Text;
                    if (string.IsNullOrWhiteSpace(this.tbApiKey.Text))
                    {
                        MessageBox.Show("Please provide Username.");
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

                    this.ExecuteOnJsonServiceClient(this.GetApiClient(serverUrl, username.ToString(), password), selectedParameter);
                }
                else if(selectedTab == this.tabAdmin)
                {
                    string serverUrl = this.tbPrincipalServer.Text;
                    if (string.IsNullOrWhiteSpace(serverUrl))
                    {
                        MessageBox.Show("Please specify Principal server.");
                        this.tbPrincipalServer.SelectAll();
                        this.tbPrincipalServer.Focus();
                        return;
                    }

                    this.ExecuteOnJsonServiceClient(this.GetAdminClient(serverUrl), selectedParameter);
                }
            }
            catch (Exception ex)
            {
                this.tbResponse.Json = ex.Message;
            }
        }

        private void ExecuteOnJsonServiceClient(JsonServiceClient client, object dto)
        {
            var parameterType = dto.GetType();
            var returnType = parameterType.GetInterfaces().FirstOrDefault();
            if (returnType != null)
            {
                string invokeMethod = this.lsRequestMethod.SelectedItem.ToString();

                if (returnType == typeof(IReturnVoid))
                {
                    var method = client.GetType().GetMethods().FirstOrDefault(m => m.Name == invokeMethod && !m.IsGenericMethod && !m.IsStatic);
                    if (method != null)
                    {
                        method.Invoke(client, new object[] { dto });
                        this.tbResponse.Json = "Request sent successfully.";
                    }
                }
                else if (returnType.IsGenericType && returnType.GetGenericTypeDefinition() == typeof(IReturn<>))
                {
                    Type returnDtoType = returnType.GetGenericArguments()[0];

                    var method = client.GetType().GetMethods().FirstOrDefault(m => m.Name == invokeMethod && m.IsGenericMethod && !m.IsStatic);
                    if (method != null)
                    {
                        var response = method.MakeGenericMethod(new Type[] { returnDtoType }).Invoke(client, new object[] { dto });
                        if (response != null)
                        {
                            JsConfig<DateTime>.SerializeFn = time => time.ToString();
                            JsConfig<DateTime?>.SerializeFn = time => time == null ? string.Empty : time.ToString();
                            this.tbResponse.Json = JsonSerializer.SerializeToString(response);
                        }
                    }
                }
            }
        }

        private void btNewKey_Click(object sender, EventArgs e)
        {
            string principalServerUrl = this.tbPrincipalServer.Text;
            if (string.IsNullOrWhiteSpace(principalServerUrl))
            {
                MessageBox.Show("Please specify Principal Server.");
                this.tbPrincipalServer.SelectAll();
                this.tbPrincipalServer.Focus();
                return;
            }

            NewApiKey dlgNewApiKey = new NewApiKey();
            if (DialogResult.OK != dlgNewApiKey.ShowDialog())
                return;

            try
            {
                using (var client = new JsonServiceClient(principalServerUrl))
                {
                    AuthResponse authResponse = client.Post(new Auth
                    {
                        UserName = "EDD8C7D1-0AC8-4AC6-B97E-F842498E8C10",
                        Password = "DED4A798-1EB2-4465-966D-7C39A1876C49",
                        provider = "internal",
                    });

                    if (authResponse.ResponseStatus.ErrorCode != null)
                    {
                        MessageBox.Show(string.Join("\n", authResponse.ResponseStatus.Errors.Select(x => x.Message)), string.Format("Error [{0}]", authResponse.ResponseStatus.ErrorCode));
                        return;
                    }

                    bool success = client.Post(new RequestCreateSubscription
                    {
                        ApiKey = dlgNewApiKey.ApiKey,
                        Username = dlgNewApiKey.Username,
                        StartDate = dlgNewApiKey.StartDate,
                        EndDate = dlgNewApiKey.ExpiredDate,
                        PaidBalance = dlgNewApiKey.PaidBalance,
                        FreeBalance = dlgNewApiKey.FreeBalance,
                    });

                    if (success)
                    {
                        MessageBox.Show(string.Format("API Key [{0}] is created.", dlgNewApiKey.ApiKey));
                        this.tbApiKey.Text = dlgNewApiKey.ApiKey.ToString().ToUpper();
                    }
                }
            }
            catch (Exception ex)
            {
                this.tbResponse.Json = ex.Message;
            }
        }

        private void tabMethod_Selected(object sender, TabControlEventArgs e)
        {
            if (this.tabMethod.SelectedTab == this.tabApi)
                this.lsApiMethod_SelectedValueChanged(this.lsApiMethod, null);
            else if (this.tabMethod.SelectedTab == this.tabAdmin)
                this.lsAdminMethod_SelectedValueChanged(this.lsAdminMethod, null);
        }

        private Lazy<SelectApiKey> dlgSearchApiKey = new Lazy<SelectApiKey>();

        private void btSelectApiKey_Click(object sender, EventArgs e)
        {
            string principalServerUrl = this.tbPrincipalServer.Text;
            if (string.IsNullOrWhiteSpace(principalServerUrl))
            {
                MessageBox.Show("Please specify Principal Server.");
                this.tbPrincipalServer.SelectAll();
                this.tbPrincipalServer.Focus();
                return;
            }

            this.dlgSearchApiKey.Value.SubscriptionQuerier = userName =>
            {
                var client = this.GetAdminClient(principalServerUrl);
                return client.Get(new RequestQuerySubscription { Username = userName });
            };

            if (DialogResult.OK == this.dlgSearchApiKey.Value.ShowDialog())
                this.tbApiKey.Text = dlgSearchApiKey.Value.SelectedApiKey;
        }

        private void btProd_Click(object sender, EventArgs e)
        {
            this.tbPrincipalServer.Text = "https://178.33.36.40/PrincipalServer/api";
            this.tbApiServer.Text = "https://api.ciiva.com/api";
        }

        private void btUat_Click(object sender, EventArgs e)
        {
            this.tbPrincipalServer.Text = "https://94.23.156.95:9143/PrincipalServer/api";
            this.tbApiServer.Text = "https://94.23.156.95:9143/ApiServer/api";
        }

        private void btDev_Click(object sender, EventArgs e)
        {
            this.tbPrincipalServer.Text = "https://94.23.156.95:9043/PrincipalServer/api";
            this.tbApiServer.Text = "https://94.23.156.95:9043/ApiServer/api";
        }

        private void btLocal_Click(object sender, EventArgs e)
        {
            this.tbPrincipalServer.Text = "https://localhost/PrincipalServer/api";
            this.tbApiServer.Text = "https://localhost/ApiServer/api";
        }
    }

    public class TypeListItem
    {
        public TypeListItem(Type t)
        {
            this.Type = t;
        }

        public Type Type { get; set; }

        public override string ToString()
        {
            return this.Type == null ? string.Empty : this.Type.FullName;
        }
    }
}