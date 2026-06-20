# Rate Limits (429 Too Many Requests)
This document outlines API rate limiting policies and mitigation strategies.

## Rate Limit Tier Structure
* **Developer Plan**: 100 requests per minute (RPM).
* **Pro Plan**: 1,000 requests per minute (RPM).
* **Enterprise Plan**: 10,000 requests per minute (RPM).

## 429 Too Many Requests Error
If a client exceeds their tier limits, the API returns a `429 Too Many Requests` status code with the following payload:
```json
{
  "error": "rate_limit_exceeded",
  "message": "API rate limit exceeded. Please back off and retry.",
  "retry_after_seconds": 30
}
```

## Response Headers
Clients must inspect headers to monitor limits:
* `X-RateLimit-Limit`: Maximum requests allowed per window.
* `X-RateLimit-Remaining`: Remaining requests in the current window.
* `X-RateLimit-Reset`: Unix timestamp when the limit resets.

**Mitigation Steps**:
1. Implement Exponential Backoff with Jitter in your client requests.
2. Read the `Retry-After` header value and wait before retrying.
3. Cache static GET requests to avoid hitting endpoints repeatedly.
