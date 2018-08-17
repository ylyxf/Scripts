using System.Collections.Generic;

namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Current price structure of a supplier component.
    /// </summary>
    public class CurrentPrice
    {
        public CurrentPrice()
        {
            this.PriceBreaks = new List<CurrentPriceBreak>();
        }

        /// <summary>
        /// Ciiva Id of supplier component to retrieve price.
        /// </summary>
        public long SupplierComponentId { get; set; }

        /// <summary>
        /// These are realtime prices.
        /// </summary>
        public bool IsRealtime { get; set; }

        /// <summary>
        /// List of price breaks.
        /// </summary>
        public List<CurrentPriceBreak> PriceBreaks { get; set; }
    }
}