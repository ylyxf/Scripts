namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Manufacturer component structure.
    /// </summary>
    public class PartNumberSuggestion
    {
        /// <summary>
        /// Manufacturer component id
        /// </summary>
        public long ManufacturerComponentId { get; set; }

        /// <summary>
        /// Manufacture name
        /// </summary>
        public string ManufacturerName { get; set; }

        /// <summary>
        /// Manufacture part number
        /// </summary>
        public string ManufacturerPartNumber { get; set; }
    }
}