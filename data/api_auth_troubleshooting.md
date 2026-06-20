# API Authentication & Authorization Troubleshooting
This guide helps resolve common OAuth2 authentication and authorization errors in CloudSync Pro.

## Common Error Payloads & Codes

### 1. 401 Unauthorized
This error occurs when the request lacks valid authentication credentials.
* **Payload Code**: `ERR_AUTH_UNAUTHORIZED`
* **Error Message**: `"Invalid or expired authentication credentials."`
* **Root Causes**:
  * The `Authorization` header is missing.
  * The Bearer token has expired or is invalid.
  * The token header prefix is incorrect.

### 2. OAuth2 Expired Tokens
OAuth2 access tokens expire after 3600 seconds (1 hour). When a token expires, clients receive a 401 Unauthorized error with the message:
`{"error": "invalid_grant", "error_description": "Token has expired"}`

**Resolution Procedure**:
1. Request a new access token using your `refresh_token`:
   `POST /oauth/token?grant_type=refresh_token&refresh_token=<REFRESH_TOKEN>`
2. Ensure token auto-renewal is enabled in your SDK configuration.

### 3. Bearer Header Mismatches
The Authorization header must match the following format exactly:
`Authorization: Bearer <token>`

* **Common Mistake**: `Authorization: token <token>` or `Authorization: Bearer<token>` (missing space).
* **Resolution**: Verify that your request headers contain a space between "Bearer" and the token.
