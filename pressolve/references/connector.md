# Pressolve Connector

The bundled Pressolve Connector is a read-only WordPress administrator tool that previews and downloads a sanitized `pressolve-report.json`. It creates no remote access, telemetry, scheduled job, database table, public endpoint, or stored export.

## Installation

1. Verify the Connector ZIP checksum and source.
2. Back up the site and install on staging first when practical.
3. Upload through **Plugins → Add New → Upload Plugin** and activate.
4. Open **Tools → Pressolve Report** as an Administrator.
5. Review the on-screen JSON before downloading or sharing it.
6. Deactivate and remove the plugin when no longer needed.

## Collected categories

- WordPress/PHP/server environment and limits
- HTTPS, debug, environment type, permalink, and search visibility state
- Active theme and plugin names/versions/slugs
- Multisite/network summary without individual-site content
- Cache/drop-in indicators
- Cron count and overdue-event count without hook arguments
- Database and autoload-size totals without option values
- REST self-check response status
- WooCommerce version and HPOS indicator when available
- A limited set of redacted fatal-error lines when `debug.log` is readable

The report intentionally excludes site URL/domain, usernames, emails, posts, orders, customers, form entries, cookies, salts, credentials, API/license keys, database values, webhook payloads, and plugin settings.

## Analysis

Treat the report as a snapshot, not proof of a root cause. Confirm timestamp/environment, run `scripts/analyze_report.py`, then correlate findings with symptoms and authoritative logs. Redact again before quoting report content.

## Security boundaries

- Require `manage_options` and a valid nonce for downloads.
- Generate the report in memory; do not save it to uploads or the database.
- Do not add remote administration, auto-fix, credential collection, or unauthenticated REST/AJAX endpoints.
- Do not execute plugin/theme code beyond normal WordPress loading.
- Do not promise that redaction catches every secret; require user preview before sharing.
- Remove the Connector after diagnosis if continuous use is unnecessary.
