using System.Collections.Generic;
using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    [Route("/4322A156-A806-4538-8D4C-8DE6FD7DE406")]
    public class GetAlternativeManufacturerComponentsById : IReturn<List<ManufacturerComponent>>
    {
        /// <summary>
        /// Id of manufacturer component.
        /// </summary>
        /// <example>
        /// Example: 128
        /// </example>
        [Category("Required")]
        [Description("Id of manufacturer component.")]
        public long ManufacturerComponentId { get; set; }

        /// <summary>
        /// Max mumber of records to return; in range 0..100.
        /// </summary>
        [Category("Required")]
        [Description("Max mumber of records to return; in range 0..100.")]
        [DefaultValue(20)]
        public int Limit { get; set; }
    }
}