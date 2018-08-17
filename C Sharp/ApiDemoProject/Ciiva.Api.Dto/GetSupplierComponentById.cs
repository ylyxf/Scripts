using System.Collections.Generic;
using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    [Route("/ECDF9BA9-C038-46D3-AFA2-E297E03B5E58")]
    public class GetSupplierComponentById : IReturn<SupplierComponent>
    {
        /// <summary>
        /// Ids of supplier components.
        /// </summary>
        [Category("Required")]
        [Description("Ids of supplier components.")]
        public long SupplierComponentId { get; set; }
    }
}