using System.Collections.Generic;
using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    [Route("/2849B6B6-8E12-4D23-84B9-4F68AA1F3457")]
    public class GetManufacturerComponentById : IReturn<ManufacturerComponentDetail>
    {
        /// <summary>
        /// Id of manufacturer component.
        /// </summary>
        [Category("Required")]
        [Description("Id of manufacturer component.")]
        public long ManufacturerComponentId { get; set; }
    }
}