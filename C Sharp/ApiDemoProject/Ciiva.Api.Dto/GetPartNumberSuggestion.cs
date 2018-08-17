using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    ///<example>
    ///Parameters:
    ///{"PW1"}
    ///
    /// Return:
    ///{ "Description" : "PW1 | Mallory Sonalert Products,
    ///  "ManufacturerComponentId" : 16,
    ///  "ManufacturerName" : "Mallory Sonalert Products",
    ///  "ManufacturerPartNumber" : "PW1"
    ///}
    ///</example>
    ///<creditcost>1</creditcost>

    [Route("/BDAA3836-DB9B-4CFE-A395-B7CBEA7B4865", Verbs = "GET, POST", Summary = "GetPartNumberSuggestion", Notes = "Get Part number suggestion.")]
    public class GetPartNumberSuggestion : IReturn<PartNumberSuggestion>
    {
        /// <summary>
        /// Manufacturer component id
        /// </summary>
        [Category("Required")]
        [Description("Part Number search keyword.")]
        public string PartNumber { get; set; }

        /// <summary>
        /// Maximum mumber of records to return; in range [0,10]
        /// </summary>
        [Category("Optional")]
        [Description("Max mumber of records to return; in range 0..10.")]
        [DefaultValue(10)]
        public int Limit { get; set; }
    }
}