# Webhook Web Handlers & Integration
This guide explains how to set up, configure, and debug webhook notifications in CloudSync Pro.

## Configuring Webhook Endpoints
To receive real-time sync conflict alerts or failure notifications:
1. Go to console > Webhooks > Add Endpoint.
2. Enter your payload URL (must use HTTPS).
3. Select events (e.g., `sync.failed`, `replica.lag_critical`).

## Webhook Retry Policy
If your endpoint returns anything other than a `2xx` HTTP status code:
* CloudSync Pro retries with exponential backoff over 24 hours.
* Total retries: 10 times.
* After 10 failures, the webhook is disabled and status is marked as `HEALTH_WARNING`.

## Debugging Payloads
All webhook requests include a signature header:
`X-CloudSync-Signature: sha256=<signature>`
Ensure your handler computes the signature of the raw body and matches this header to verify authenticity.
Example of a valid webhook endpoint configuration is available in our developer SDK.
Refrain from sending unencrypted payloads over HTTP.
