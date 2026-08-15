# Headless WordPress and Integrations

## Headless architecture

Define content ownership, rendering strategy, preview/draft workflow, authentication, cache/invalidation, media, search, forms, SEO metadata, redirects, localization, deployment, failure behavior, and editor expectations before choosing tools.

For REST or GraphQL:

- Expose only required fields and enforce capabilities.
- Validate schema/input, pagination, filtering, and rate limits.
- Avoid leaking drafts, private meta, user data, or secrets.
- Plan cache tags/keys and invalidation for create/update/delete events.
- Make preview tokens short-lived and environment-specific.
- Preserve canonical URLs, sitemap, structured data, and redirect ownership.

## Authentication

Choose cookie/nonce authentication for same-origin WordPress admin flows, application passwords or OAuth-style mechanisms for approved server integrations, and provider-supported methods for third parties. Never place long-lived privileged WordPress credentials in browser code.

## Webhooks and automation

For CRM, Zapier, Make, email, search, analytics, inventory, or custom APIs:

1. Define event source and authoritative system.
2. Verify signatures and permissions.
3. Use idempotency keys/stable object IDs.
4. Set timeouts, retry/backoff, dead-letter/manual recovery, and replay controls.
5. Redact logs and store secrets outside code/database exports where possible.
6. Prevent loops between bidirectional systems.
7. Test duplicates, out-of-order delivery, partial failure, and provider outage.

## Integration diagnosis

Trace the complete lifecycle: WordPress event, queue/scheduler, outbound request, provider response, webhook callback, local update, and user-visible state. Correlate timestamps and IDs without exposing payload secrets or personal data.

Do not resend production webhooks, campaigns, payments, or destructive synchronization events without explicit authorization.
