using System;
using System.Collections.Generic;

namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Stock structure of an supplier component.
    /// </summary>
    public class Stock
    {
        public Stock()
        {
            this.StockItems = new List<StockItem>();
        }

        /// <summary>
        /// Id of supplier component.
        /// </summary>
        public long SupplierComponentId { get; set; }

        /// <summary>
        /// Detail stock info.
        /// </summary>
        public List<StockItem> StockItems { get; set; }
    }
}