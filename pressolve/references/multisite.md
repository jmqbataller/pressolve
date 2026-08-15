# WordPress Multisite

## Establish network context

Identify subdomain or subdirectory mode, Network Admin access, domain mapping, sunrise/drop-ins, hosting/DNS topology, network-active plugins, allowed themes, site count, user model, upload paths, database scale, and backup/restore capabilities.

Distinguish:

- Network settings versus individual-site settings
- Super Admin versus site Administrator permissions
- Network-activated versus per-site plugins
- Shared code/core versus separate uploads and site tables
- Main-site/domain behavior versus mapped domains

## Diagnosis

For a site-specific issue, compare the affected site's theme, active plugins, options, domain mapping, users, uploads, and cache variant with a working site. For network-wide failures, check network-active code, must-use plugins, drop-ins, domain/cookie constants, database connectivity, rewrites, cron, and recent network changes.

Do not deactivate a network plugin or theme without assessing every dependent site.

## Domain mapping and SSL

Inventory nameserver and DNS records, proxy/CDN state, certificate coverage, canonical host, HTTP-to-HTTPS redirects, `home`/`siteurl`, cookie domain/path, and reverse-proxy headers. Verify each mapped domain independently and preserve email DNS records.

## Network operations

- Use WP-CLI network/site/user commands only after confirming the target network and site ID.
- State whether commands operate globally or per site.
- Take a network-aware backup before bulk activation, search-replace, user changes, or site deletion.
- Avoid direct edits to global tables or per-site tables unless WordPress APIs/WP-CLI cannot perform the operation safely.

For site-scoped cron checks, first list sites and then run read-only commands with an explicit site URL, for example `wp site list --fields=blog_id,url` followed by `wp cron event list --url='https://mapped.example/' --fields=hook,next_run_gmt,next_run_relative,recurrence`. Compare an affected site, a working peer, and the main site. Inspect WooCommerce Scheduled Actions from the selected site's dashboard or a verified site-scoped command. Do not run overdue events merely to test them; they may charge renewals, modify orders, send email, or call webhooks.

## Migration

Map network tables, per-site tables, blogs/site IDs, uploads, domain/path values, salts/cookies, sunrise/domain-mapping behavior, cron, and SSL. Use serialized-safe replacement and validate main site, several representative subsites, mapped domains, login, media, roles, forms, and cache isolation.

Converting single-site to multisite or extracting a subsite is a data migration, not a normal URL change. Document unsupported plugin behavior and reconciliation requirements before proceeding.
