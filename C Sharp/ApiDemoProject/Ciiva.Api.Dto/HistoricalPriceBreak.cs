using System;

namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Historial price structure.
    /// </summary>
    public class HistoricalPriceBreak
    {
        /// <summary>
        /// Start date.
        /// </summary>
        public DateTime? StartDate { get; set; }

        /// <summary>
        /// End date.
        /// </summary>
        public DateTime? EndDate { get; set; }

        /// <summary>
        /// MinQuantity
        /// </summary>
        public int? MinQuantity { get; set; }

        /// <summary>
        /// UnitPrice
        /// </summary>
        public decimal? UnitPrice { get; set; }

        /// <summary>
        /// Currency name.
        /// </summary>
        public string CurrencyName { get; set; }

        /// <summary>
        /// Location name.
        /// </summary>
        public string LocationName { get; set; }
    }
}