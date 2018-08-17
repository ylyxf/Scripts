using System.Collections.Generic;
using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    [Route("/DFA2EB61-10A6-411B-9188-FEF7E6151F25")]
    public class GetSupplierComponentsByPartNumber : IReturn<List<SupplierComponent>>
    {
        /// <summary>
        /// Supplier name.
        /// </summary>
        [Category("Required")]
        [Description("Supplier name.")]
        public string SupplierName { get; set; }

        /// <summary>
        /// Supplier part number.
        /// </summary>
        [Category("Required")]
        [Description("Supplier part number.")]
        public string SupplierPartNumber { get; set; }

        /// <summary>
        /// Exact match.
        /// </summary>
        [Category("Optional")]
        [Description("Exact match.")]
        [DefaultValue(false)]
        public bool ExactMatch { get; set; }

        /// <summary>
        /// Max mumber of records to return; in range 0..100.
        /// </summary>
        [Category("Required")]
        [Description("Max mumber of records to return; in range 0..100.")]
        [DefaultValue(5)]
        public int Limit { get; set; }
    }
}