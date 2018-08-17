using System.Collections.Generic;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    [Route("/428298F5-913C-4300-94B5-EF951F283C04")]
    public class GetExchangeRates : IReturn <List<ExchangeRateItem>>
    {
    }
}