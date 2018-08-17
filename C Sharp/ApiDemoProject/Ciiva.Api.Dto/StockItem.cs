using System;
using System.Collections.Generic;

namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Detail stock info structure.
    /// </summary>
    public class StockItem
    {
        /// <summary>
        /// Location name.
        /// </summary>
        public string LocationName { get; set; }

        /// <summary>
        /// Quantity
        /// </summary>
        public decimal Quantity { get; set; }

        /// <summary>
        /// Lead time.
        /// </summary>
        public string LeadTime { get; set; }

        /// <summary>
        /// Valid date.
        /// </summary>
        public DateTime? ValidDate { get; set; }
    }
}