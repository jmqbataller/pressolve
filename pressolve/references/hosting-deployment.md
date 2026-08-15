# Hosting, DNS, Email, Migration, and Deployment

## Hosting and PHP

Check current resource graphs and logs before recommending a larger memory limit or plan. Distinguish PHP memory, upload limits, request timeouts, PHP workers, CPU throttling, disk/inodes, database limits, and external API latency.

When changing PHP versions, verify WordPress, theme, plugin, ionCube/vendor requirements, deprecated functions, cron, CLI, and background jobs on staging first.

## DNS, CDN, and SSL

Record current DNS records and proxy status before edits. Explain propagation as resolver caching governed by TTL, not as a guaranteed waiting period. Check A/AAAA/CNAME consistency, nameserver delegation, origin reachability, certificate hostname/chain, redirects, mixed content, and CDN SSL mode.

Avoid exposing an origin or bypassing security controls without authorization. Preserve mail-related MX, SPF, DKIM, and DMARC records during domain changes.

## Transactional email

Trace message generation, SMTP/API acceptance, authentication alignment, bounce/suppression state, and recipient delivery. Recommend a transactional provider instead of relying on unauthenticated PHP mail for important messages. Redact message content and recipient data from reports unless necessary.

## Backups and migrations

A usable backup includes the database, uploads, custom code, configuration, and a documented restore path. Before migration:

1. Inventory domain, DNS, SSL, PHP, cron, email, cache/CDN, redirects, integrations, and storage.
2. Confirm source and destination requirements and available rollback time.
3. Freeze or reconcile changing data such as orders, forms, and memberships.
4. Migrate, perform serialized-safe URL replacement, and preserve identifiers/permissions.
5. Test through a hosts-file or staging URL when practical.
6. Cut over DNS with monitoring and retain the source during rollback window.
7. Verify critical journeys, cron, email, webhooks, analytics, SEO directives, and backups.

Never use plain SQL replacement on serialized WordPress data. Prefer WP-CLI or a trusted migration tool.

## WP-CLI and deployment

State the target environment and working directory before commands. Use dry runs where supported. Back up before database operations. Avoid commands that activate, delete, search-replace, flush, regenerate, or run due events on production without explicit authorization.

For Git-based deployments, keep secrets and uploads out of source control, make environment configuration explicit, build reproducibly, and provide rollback to the previous artifact/database state.
