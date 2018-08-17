namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Price break structure.
    /// </summary>
    public class CurrentPriceBreak
    {
        /// <summary>
        /// Mininum order quantity to acquire this unit price.
        /// </summary>
        public int MinQuantity { get; set; }

        /// <summary>
        /// Unit price.
        /// </summary>
        public decimal UnitPrice { get; set; }

        /// <summary>
        /// Currency name.
        /// </summary>
        public string CurrencyName { get; set; }

        /// <summary>
        /// Location of sale.
        /// </summary>
        public string LocationName { get; set; }
    }
}