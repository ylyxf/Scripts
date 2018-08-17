using System.Collections.Generic;
using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Present request for matching BOM.
    /// </summary>
    [Route("/65E70374-793C-4BA4-B87D-008474FCD3E9")]
    public class GetManufacturerComponentsByDescriptiveSearch : IReturn<List<ManufacturerComponent>>
    {
        /// <summary>
        /// Search key words.
        /// </summary>
        [Category("Required")]
        [Description("Search key words.")]
        public string Description { get; set; }

        /// <summary>
        /// Max mumber of records to return; in range 0..100.
        /// </summary>
        [Category("Required")]
        [Description("Max mumber of records to return; in range 0..100.")]
        [DefaultValue(20)]
        public int Limit { get; set; }
    }
}