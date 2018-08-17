using System.Collections.Generic;
using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    [Route("/006F09E5-32A6-4516-A56D-41883DDE9D23")]
    public class GetManufacturerComponentsByPartNumber : IReturn<List<ManufacturerComponentDetail>>
    {
        /// <summary>
        /// Manufacturer name.
        /// </summary>
        [Category("Required")]
        [Description("Manufacturer name.")]
        public string ManufacturerName { get; set; }

        /// <summary>
        /// Manufacturer part number.
        /// </summary>
        [Category("Required")]
        [Description("Manufacturer part number.")]
        public string ManufacturerPartNumber { get; set; }

        /// <summary>
        /// Exact match.
        /// </summary>
        [Category("Optional")]
        [Description("Exact match.")]
        [DefaultValue(false)]
        public bool ExactMatch { get; set; }

        /// <summary>
        /// Include Technical details in result.
        /// </summary>
        [Category("Optional")]
        [Description("Include Technical details in result.")]
        [DefaultValue(false)]
        public bool ExtraInfo { get; set; }

        /// <summary>
        /// Max mumber of records to return; in range 0..100.
        /// </summary>
        [Category("Required")]
        [Description("Max mumber of records to return; in range 0..100.")]
        [DefaultValue(5)]
        public int Limit { get; set; }
    }
}