=== Pressolve Connector ===
Contributors: jmqbataller
Tags: diagnostics, site health, troubleshooting, wordpress
Requires at least: 6.5
Requires PHP: 7.4
Stable tag: 2.1.0
License: MIT
License URI: https://opensource.org/license/mit

Read-only, administrator-only diagnostic export for the Pressolve AI WordPress Website Specialist.

== Description ==

Pressolve Connector previews and downloads a sanitized pressolve-report.json. It stores no report, creates no public endpoint, sends no telemetry, and provides no remote administration.

The report includes environment versions and limits, active plugin/theme names and versions, cache indicators, cron totals, database/autoload size totals, a REST self-check, WooCommerce compatibility indicators, and a limited set of redacted fatal-error lines when debug.log is readable.

The report excludes URLs/domains, usernames, posts, orders, customers, form entries, cookies, salts, credentials, API/license keys, option values, and webhook payloads. Always review the preview before sharing it.

== Installation ==

1. Upload and activate the plugin.
2. Open Tools > Pressolve Report as an Administrator.
3. Review the JSON preview.
4. Download and upload the JSON to Pressolve when ready.
5. Deactivate and remove the plugin when diagnosis is complete.

== Privacy ==

The plugin does not transmit or persist diagnostic data. Generating a report performs one short REST self-check against the same WordPress site.

== Changelog ==

= 2.1.0 =
* Aligns the Connector package with Pressolve Live Site Audit and the v2.1 suite release.

= 2.0.0 =
* Initial read-only diagnostic connector release.
