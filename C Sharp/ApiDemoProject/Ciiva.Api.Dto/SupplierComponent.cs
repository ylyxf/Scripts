using System.Collections.Generic;

namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Supplier component structure.
    /// </summary>
    public class SupplierComponent
    {
        /// <summary>
        /// Id of manufacturer component.
        /// </summary>
        public long ManufacturerComponentId { get; set; }

        /// <summary>
        /// Id of supplier component.
        /// </summary>
        public long SupplierComponentId { get; set; }

        /// <summary>
        /// Supplier name.
        /// </summary>
        public string SupplierName { get; set; }

        /// <summary>
        /// Supplier part number.
        /// </summary>
        public string SupplierPartNumber { get; set; }

        /// <summary>
        /// Description.
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Authorised component.
        /// </summary>
        public bool IsAuthorised { get; set; }

        /// <summary>
        /// Datasheet Url.
        /// </summary>
        public string DatasheetUrl { get; set; }

        /// <summary>
        /// Detail Url.
        /// </summary>
        public string DetailUrl { get; set; }
    }
}