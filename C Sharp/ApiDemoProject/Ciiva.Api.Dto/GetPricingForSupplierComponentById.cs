using System.Collections.Generic;
using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    [Route("/D65797C8-DCAA-466F-8377-0ED6730533D4")]
    public class GetPricingForSupplierComponentById : IReturn<List<CurrentPrice>>
    {
        /// <summary>
        /// Id of supplier component.
        /// </summary>
        [Category("Required")]
        [Description("Id of supplier component.")]
        public long SupplierComponentId { get; set; }

        /// <summary>
        /// Query realtime prices.
        /// </summary>
        [Category("Optional")]
        [Description("Query realtime prices.")]
        [DefaultValue(false)]
        public bool? UseRealTime { get; set; }
    }
}