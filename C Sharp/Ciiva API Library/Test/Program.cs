using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CiivaApis;

namespace Test
{
    class Program
    {
        static void Main(string[] args)
        {
            var ciivaAPI = new Apis();
            var client = ciivaAPI.GetApiClient();
            ciivaAPI.GetSupplierComponentsByPartNumber("Digi-Key", "887-1271-1-ND", client);
            string x = ciivaAPI.queryResult;
            Console.WriteLine(ciivaAPI.queryResult);

        }
    }
}
