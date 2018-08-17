using System.Collections.Generic;
using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    [Route("/A7BAAA4D-45FF-4072-8AD8-FDC411CC179A")]
    public class GetPricingForMultipleSupplierComponentsById : IReturn<List<CurrentPrice>>
    {
        public GetPricingForMultipleSupplierComponentsById()
        {
            this.SupplierComponentIds = new List<long>();
        }

        /// <summary>
        /// List of Ids of supplier components.
        /// </summary>
        [Category("Requried")]
        [Description("List of Ids of supplier components.")]
        public List<long> SupplierComponentIds { get; set; }

        /// <summary>
        /// Query realtime prices.
        /// </summary>
        [Category("Optional")]
        [Description("Query realtime prices.")]
        [DefaultValue(false)]
        public bool? UseRealTime { get; set; }
    }
}