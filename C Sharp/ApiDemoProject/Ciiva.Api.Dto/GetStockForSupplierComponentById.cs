using System.Collections.Generic;
using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    [Route("/C9F1E722-D93D-4D2E-A909-E4EBB1917214")]
    public class GetStockForSupplierComponentById : IReturn<List<Stock>>
    {
        /// <summary>
        /// Id of supplier component.
        /// </summary>
        [Category("Required")]
        [Description("Id of supplier component.")]
        public long SupplierComponentId { get; set; }      
 
        /// <summary>
        /// Query realtime stock info.
        /// </summary>
        [Category("Optional")]
        [Description("Query realtime stock info.")]
        [DefaultValue(false)]
        public bool? UseRealTime { get; set; }
    }
}