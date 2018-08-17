namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Exchange rate structure.
    /// </summary>
    public class ExchangeRateItem
    {
        /// <summary>
        /// Currency name.
        /// </summary>
        public string CurrencyName { get; set; }

        /// <summary>
        /// ExchangeRate.
        /// </summary>
        public decimal ExchangeRate { get; set; }

        /// <summary>
        /// Acronym
        /// </summary>
        public string Acronym { get; set; }
    }
}