# Pressolve Live Site Audit

Use this workflow when the user pastes a WordPress website URL and asks for its status, health, quality, errors, or a whole-site review. Start the public audit immediately when a valid URL is supplied; do not require WordPress login details.

## Set the boundary

Treat the URL as a public, read-only production target unless the user says otherwise. Use ordinary page requests and browser navigation only. By default inspect at most eight representative HTML pages: the homepage, then high-value About, Services, Contact, Shop/Product, Blog/News, Listing, and policy page types discovered through navigation or declared sitemaps. Never exceed 20 pages unless the user explicitly requests a broader authorized audit. Respect `robots.txt` crawl restrictions.

Never sign in, guess credentials, enumerate hidden paths, bypass a WAF, exploit a suspected vulnerability, submit forms, create carts/orders/accounts, trigger searches repeatedly, or call endpoints that change data. Do not fetch customer records or private REST data. If the site blocks the audit, report the result as incomplete rather than bypassing the block.

## Run the public audit

1. Resolve the supplied URL, redirect chain, canonical host, HTTPS state, certificate validity, and homepage status.
2. Inspect the homepage and representative pages from navigation or declared sitemaps. Include the main conversion page types, but do not submit their forms or checkout flows.
3. Record 4xx/5xx responses, redirect loops, visible error states, mixed-content requests, broken rendered assets, and browser console/network errors when browser tooling is available.
4. Check `robots.txt`, WordPress core/SEO sitemap locations, canonical tags, index directives, titles, descriptions, language, viewport, headings, image alternative-text attributes, and structured-data clues.
5. Look for WordPress evidence such as `wp-content`, `wp-includes`, REST discovery, `/wp-json/`, or generator metadata. Report a confidence level; absence of these clues does not prove the site is not WordPress.
6. Check cache/CDN and defensive-header signals. Treat missing headers as configuration observations whose impact depends on the site; do not label every missing header a vulnerability.
7. Inspect desktop and mobile rendering, navigation, focus/keyboard behavior, overflow, dialogs, cookie banners, and visible forms without submitting data.
8. Run Lighthouse or an equivalent synthetic audit when available. Label it as lab data, record the tested URL/device/time, and do not present one score as field Core Web Vitals. Field and lab data can differ.
9. Use `scripts/live_site_audit.py <url>` when local execution and outbound network access are available. Review its JSON, then corroborate important findings in the rendered site.

When the environment cannot expose response headers, emulate mobile, run Lighthouse, resolve the target for the bundled scanner, or open a declared endpoint, mark that check **Not tested** and continue with the evidence available. Do not substitute inference. Offer a precise follow-up such as uploading a Lighthouse JSON report, browser HAR, response-header output, screenshot, Site Health export, or Connector report.

WordPress REST discovery and sitemap behavior are documented by [WordPress REST API Discovery](https://developer.wordpress.org/rest-api/using-the-rest-api/discovery/) and [`WP_Sitemaps`](https://developer.wordpress.org/reference/classes/wp_sitemaps/). Lighthouse covers performance, accessibility, best practices, and SEO, but synthetic results need context; see the [official Lighthouse overview](https://developer.chrome.com/docs/lighthouse/overview) and [lab-versus-field guidance](https://web.dev/articles/lab-and-field-data-differences).

## Interpret WordPress clues carefully

Public asset paths can reveal plugin or theme slugs, but they are not a complete installed or active inventory. They do not prove the installed version, maintenance state, exploitability, or root cause. Verify version-sensitive conclusions through the Connector, Site Health, authorized admin evidence, or official vendor documentation.

Do not probe author/user endpoints merely to enumerate accounts. A reachable REST index is normal WordPress functionality and is not automatically a security defect.

## Separate public and deep checks

| Public URL can verify | Requires Connector or authorized access |
|---|---|
| Current public response and rendered state | Uptime history and server resource graphs |
| Redirects, HTTPS, certificate, public headers | PHP configuration, workers, opcode cache, and server logs |
| Public pages, metadata, sitemap, and robots | Complete plugin/theme inventory and exact versions |
| Visible responsive, console, and accessibility issues | Admin/editor behavior, roles, updates, and Site Health |
| Passive form and checkout presentation | Email delivery, payment processing, orders, and webhook results |
| Synthetic performance snapshot | Real-user Core Web Vitals and long-term trends |
| WordPress and public asset clues | Database health, cron, autoload, fatal logs, malware, and backups |

Offer the Pressolve Connector only when the user wants the deeper column. Explain what it collects before installation.

## Report format

Lead with one status: **Healthy**, **Needs attention**, **Degraded**, **Critical**, or **Incomplete**. Include timestamp, canonical URL, tested page count, device/context, and limitations.

Then return:

1. Executive status and observed impact
2. Page/status matrix
3. Critical and High findings
4. Medium and Low improvements
5. WordPress detection confidence and public clues
6. Performance, SEO, accessibility, security-header, and responsive summaries
7. Checks that were not possible from a public URL
8. Exact next actions and verification criteria

For every finding, distinguish **Observed**, **Supported**, **Inferred**, or **Not tested**. Do not say the whole website is healthy when only a sample was inspected.
