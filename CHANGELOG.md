# Changelog

All notable Pressolve changes are recorded here.

## [2.1.0] - 2026-08-15

### Added

- Pressolve Live Site Audit mode for pasted WordPress or website URLs.
- Bounded public checks for redirects, HTTPS/certificate state, representative page responses, WordPress signals, REST discovery, robots, sitemaps, metadata, headings, image alt attributes, mixed content, cache/security headers, and public plugin/theme asset clues.
- Safe `live_site_audit.py` JSON scanner with private-network blocking, redirect validation, crawl limits, `robots.txt` handling, sensitive-path exclusions, and offline self-tests.
- Public-versus-deep audit matrix so results clearly identify which checks require the Pressolve Connector, WordPress admin, hosting logs, or field monitoring.
- Live-audit reporting states: Healthy, Needs attention, Degraded, Critical, and Incomplete.

### Changed

- Updated Pressolve triggering and default prompt to recognize a pasted website URL as an audit request.
- Aligned the Connector and release packages with the v2.1 suite.
- Added release-time self-testing for the new public scanner.

## [2.0.0] - 2026-08-15

### Added

- Pressolve Scan for sanitized diagnostic bundles, Site Health exports, logs, HAR files, Lighthouse reports, screenshots, and Connector JSON.
- Deterministic `pressolve-report.json` analyzer with prioritized findings and human-review guardrails.
- Pressolve Lab with a conservative WordPress Playground Blueprint generator.
- Update Guard compatibility matrices, update sequencing, staging decisions, rollback limits, and reconciliation planning.
- Dedicated Multisite, Block Studio, monitoring/privacy, content migration, headless/integrations, and business-site specialist packs.
- Modern block-theme, `theme.json`, custom/dynamic block, pattern, binding, hook, and Interactivity API guidance.
- Membership, LMS, booking, subscription, directory, marketplace, multilingual, nonprofit, and agency-maintenance workflows.
- Read-only Pressolve Connector WordPress plugin with administrator preview and in-memory sanitized JSON download.
- Separate Connector ZIP and SHA-256 checksum in GitHub Releases.

### Changed

- Expanded Pressolve operating modes with Scan, Guard, Lab, and Monitor.
- Updated the release builder to package both the ChatGPT skill and WordPress Connector reproducibly.
- Strengthened untrusted-artifact, privacy, monitoring, incident-response, and production-safety rules.

## [1.0.0] - 2026-08-15

### Added

- Initial Pressolve AI WordPress Website Specialist skill.
- Ask, Diagnose, Recommend, Build, Audit, and Handover operating modes.
- Evidence-first troubleshooting and production safety workflow.
- Plugin, theme, template, child-theme, and update guidance.
- Gutenberg, Elementor, Bricks, Divi, forms, and WooCommerce guidance.
- Performance, caching, security, hosting, DNS, SSL, email, and migration guidance.
- WordPress custom-development security and implementation checklist.
- Technical SEO and accessibility review guidance.
- IDX, MLS, RESO, property-search, and real-estate website specialization.
- Website QA and client-ready audit reporting.
- Reproducible ZIP packaging with SHA-256 checksum.
- Automated GitHub Release publishing.
