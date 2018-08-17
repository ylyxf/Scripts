namespace Ciiva.Api.Dto
{
    /// <summary>
    /// Authentication response.
    /// </summary>
    public class AuthenticationResponse
    {
        /// <summary>
        /// SessionId must be attahed to subsequence requests sending to server for validation.
        /// </summary>
        public string SessionId { get; set; }

        /// <summary>
        /// Username has been authenticated successfully with the SessionId.
        /// </summary>
        public string Username { get; set; }
    }
}