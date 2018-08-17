using System;

namespace Ciiva.Api.Dto
{
    public class SubscriptionStatus
    {
        public double FreeBalance { get; set; }

        public DateTime FreeExpireDate { get; set; }

        public double PaidBalance { get; set; }

        public DateTime PaidExpireDate { get; set; }
    }
}