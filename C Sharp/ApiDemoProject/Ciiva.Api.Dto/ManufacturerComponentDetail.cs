using System.Collections.Generic;

namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Manufacturer component structure.
    /// </summary>
    public class ManufacturerComponentDetail
    {
        public ManufacturerComponentDetail()
        {
            this.ManufacturerNameAlias = new List<string>();
            this.TechnicalDetails = new List<TechnicalDetail>();
        }

        /// <summary>
        /// Description
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Manufacturer component id
        /// </summary>
        public long ManufacturerComponentId { get; set; }

        /// <summary>
        /// Manufacture name
        /// </summary>
        public string ManufacturerName { get; set; }

        /// <summary>
        /// Alternative names of this manufacturer
        /// </summary>
        public List<string> ManufacturerNameAlias { get; set; }

        /// <summary>
        /// Manufacturer Part Image URL
        /// </summary>
        public string ManufacturerPartImageURL { get; set; }

        /// <summary>
        /// Manufacture part number
        /// </summary>
        public string ManufacturerPartNumber { get; set; }

        /// <summary>
        /// Manufacturer Part URL
        /// </summary>
        public string ManufacturerPartURL { get; set; }

        /// <summary>
        /// Life cycle status id
        /// </summary>
        public int? LifeCycleStatusId { get; set; }

        /// <summary>
        /// Life cycle status
        /// </summary>
        public string LifeCycleStatusName { get; set; }

        /// <summary>
        /// Technical details.
        /// </summary>
        public List<TechnicalDetail> TechnicalDetails { get; set; }
    }
}