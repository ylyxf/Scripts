using System.Collections.Generic;
using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    [Route("/A5C66425-5BFC-4CD5-AAC9-CF8B6B52A14B")]
    public class GetSupplierComponentsByManufacturerComponentId : IReturn<List<SupplierComponent>>
    {
        /// <summary>
        /// Id of manufacturer component.
        /// </summary>
        [Category("Required")]
        [Description("Id of manufacturer component.")]
        public long ManufacturerComponentId { get; set; }

        /// <summary>
        /// Max mumber of records to return; in range 0..100.
        /// </summary>
        [Category("Required")]
        [Description("Max mumber of records to return; in range 0..100.")]
        [DefaultValue(5)]
        public int Limit { get; set; }
    }
}