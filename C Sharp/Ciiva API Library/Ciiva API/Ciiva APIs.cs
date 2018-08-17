using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ServiceStack.Common.ServiceClient.Web;
using ServiceStack.ServiceClient.Web;
using ServiceStack.ServiceHost;
using ServiceStack.Text;
using Ciiva.ApiServer.SVS.ClientDto;

namespace CiivaApis
{
    public class Apis
    {
        public JsonServiceClient GetApiClient()
        {
            string baseUri = "https://api.ciiva.com/api";
            string username = "ded47940-ca3e-4792-86e9-7c5777924c40";
            string password = "Altium1!";
            JsonServiceClient apiClient = null;
            
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
                    Console.WriteLine(string.Join("\n", authResponse.ResponseStatus.Errors.Select(x => x.Message)), string.Format("Error [{0}]", authResponse.ResponseStatus.ErrorCode));
                else
                    apiClient = client;
            }

            return apiClient;


        }

        public string queryResult = "";

        private void ExecuteOnJsonServiceClient(JsonServiceClient client, object dto)
        {
            var parameterType = dto.GetType();
            var returnType = parameterType.GetInterfaces().FirstOrDefault();
            if (returnType != null)
            {
                string invokeMethod = "Post";

                if (returnType == typeof(IReturnVoid))
                {
                    var method = client.GetType().GetMethods().FirstOrDefault(m => m.Name == invokeMethod && !m.IsGenericMethod && !m.IsStatic);
                    if (method != null)
                    {
                        method.Invoke(client, new object[] { dto });
                        Console.WriteLine("Request sent successfully.");
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
                            queryResult = JsonSerializer.SerializeToString(response);
                        }
                    }
                }
            }
        }

        public void GetSupplierComponentsByPartNumber(string supplierName, string supplierPartNumber, JsonServiceClient client)
        {
            var getSupplierCommponent = new GetSupplierComponentsByPartNumberRequest();
            getSupplierCommponent.ExactMatch = false;
            getSupplierCommponent.Limit = 1;
            getSupplierCommponent.Start = 0;
            getSupplierCommponent.SupplierName = supplierName;
            getSupplierCommponent.SupplierPartNumber = supplierPartNumber;

            ExecuteOnJsonServiceClient(client, getSupplierCommponent);
        }

        public void GetManufacturerComponentsByPartNumberRequest(string ManufacturerName, string ManufacturerPartNumber, JsonServiceClient client)
        {
            var getManuFacturerComponent = new GetManufacturerComponentsByPartNumberRequest();
            getManuFacturerComponent.ExactMatch = true;
            getManuFacturerComponent.Limit = 5;
            getManuFacturerComponent.ManufacturerName = ManufacturerName;
            getManuFacturerComponent.ManufacturerPartNumber = ManufacturerPartNumber;

            ExecuteOnJsonServiceClient(client, getManuFacturerComponent);
        }

        public void GetManufacturerComponentById(long ManufacturerComponentId, JsonServiceClient client)
        {
            var getManufacturerComponentId = new GetManufacturerComponentByIdRequest();
            getManufacturerComponentId.ManufacturerComponentId = ManufacturerComponentId;

            ExecuteOnJsonServiceClient(client, getManufacturerComponentId);
        }
            


    }
}
