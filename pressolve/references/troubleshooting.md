# Troubleshooting and Recovery

## Triage order

1. Confirm the exact failure, affected URLs/users/devices, and when it began.
2. Capture the current state before clearing caches, disabling components, or changing configuration.
3. Check recent deploys, updates, content edits, DNS/CDN changes, PHP changes, and hosting incidents.
4. Identify whether the frontend, wp-admin, cron, REST API, email, or the entire origin is affected.
5. Test one variable at a time and record the result.

## Evidence collection

Request only what is relevant:

- WordPress Site Health status and versions
- Browser console and failed Network requests
- WordPress debug log with secrets and personal data redacted
- PHP/web-server error log around the failure timestamp
- Active theme, must-use plugins, drop-ins, and active plugins
- Exact error text and reproduction steps
- Hosting resource limits, PHP memory, upload limits, and timeout values
- DNS results, SSL certificate chain, CDN response headers, or email delivery logs

Enable logging on a staging site or for the shortest practical production window. Do not display PHP errors to public visitors. Restore the prior debug configuration after collection.

## Common failure patterns

| Symptom | First evidence | Likely layers | Safe first test |
|---|---|---|---|
| Critical error or blank page | PHP error log | Plugin, theme, PHP compatibility, memory | Identify the fatal file and line before disabling anything |
| wp-admin inaccessible | HTTP status, server log | Plugin, security rule, redirect, cookies | Test an incognito session and inspect the redirect/network chain |
| Builder loads forever | Console/network errors | Plugin conflict, REST/AJAX, cache, browser extension | Test Safe Mode/staging and inspect failed REST/AJAX requests |
| 500/503 response | Origin error log, resource graphs | PHP fatal, timeout, worker/resource exhaustion | Bypass CDN only if authorized and compare origin behavior |
| Database connection error | Host/database status, wp-config values | Database outage, credential/config issue, exhausted connections | Confirm service health without exposing credentials |
| Changes not visible | Cache headers and purge history | Browser, page cache, object cache, CDN | Purge one layer at a time and verify headers |
| Email not delivered | Form log, SMTP/provider log | Form config, SMTP, DNS authentication, suppression | Send a controlled test and trace provider acceptance |
| Scheduled task missed | Cron event list, loopback status | WP-Cron disabled, low traffic, loopback failure | Inspect due events and cron configuration before running jobs |

## Plugin/theme conflict isolation

Prefer a staging clone, hosting troubleshooting mode, or a tool that disables components only for the current administrator session. If unavailable:

1. Verify a backup and maintenance window.
2. Record active plugins, theme, widgets, menus, template conditions, and cache configuration.
3. Disable the most recently changed or error-linked component first.
4. If needed, test with nonessential plugins disabled and a default theme.
5. Restore components in small groups, then individually identify the trigger.
6. Check whether the conflict is configuration-specific before replacing a product.
7. Restore the original state if the test is inconclusive.

Do not disable payment, membership, security, backup, multilingual, or data-sync plugins on production without understanding the operational impact.

## Recovery principles

- Put availability and data preservation ahead of diagnosis completeness.
- Take a fresh database snapshot before restoring files or running search-and-replace.
- Match database and uploads to the same recovery point when consistency matters.
- After recovery, verify login, forms, transactions, cron, webhooks, cache, and monitoring.
- Preserve logs and a timeline for root-cause analysis.
- When compromise is suspected, rotate affected credentials from a clean device, preserve evidence, and involve the host or a qualified incident responder.
