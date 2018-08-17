using System.Collections.Generic;

namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Historical price struct of an supplier component.
    /// </summary>
    public class HistoricalPrice
    {
        public HistoricalPrice()
        {
            this.PriceBreaks = new List<HistoricalPriceBreak>();
        }

        /// <summary>
        /// Id of supplier component.
        /// </summary>
        public long SupplierComponentId { get; set; }

        /// <summary>
        /// Price breaks.
        /// </summary>
        public List<HistoricalPriceBreak> PriceBreaks { get; set; }
    }
}