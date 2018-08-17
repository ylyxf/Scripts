using System.Collections.Generic;
using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    [Route("/46FC821A-B0A1-423F-B446-1372BA7A95B6")]
    public class GetStockForMultipleSupplierComponentsById : IReturn<List<Stock>>
    {
        public GetStockForMultipleSupplierComponentsById()
        {
            this.SupplierComponentIds = new List<long>();
        }

        /// <summary>
        /// List of Ids of supplier components.
        /// </summary>
        [Category("Required")]
        [Description("List of Ids of supplier components.")]
        public List<long> SupplierComponentIds { get; set; }

        /// <summary>
        /// Query realtime stock info.
        /// </summary>
        [Category("Optional")]
        [Description("Query realtime stock info.")]
        [DefaultValue(false)]
        public bool? UseRealTime { get; set; }
    }
}