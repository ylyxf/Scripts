using System.ComponentModel;
using ServiceStack.ServiceHost;

namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Authentication request.
    /// </summary>
    [Route("/auth/apikey", Verbs = "GET, POST", Summary = "Authentication", Notes = "")]
    public class AuthenticationRequest : IReturn<AuthenticationResponse>
    {
        /// <summary>
        /// Use API Key to authenticate.
        /// </summary>
        [Description("Use API Key to authenticate.")]
        public string Username { get; set; }

        /// <summary>
        /// Password to authenticate.
        /// </summary>
        [Description("Password to authenticate.")]
        public string Password { get; set; }
    }
}