# Monitoring, Maintenance, Privacy, and Incidents

## Monitoring plan

Define owner, frequency, alert channel, threshold, evidence, and response for:

- Availability and representative user journeys
- SSL and domain expiration
- Backup completion and restore tests
- WordPress/PHP/plugin/theme support and security updates
- PHP fatals, server errors, resource limits, and disk/inodes
- Failed cron/Action Scheduler jobs and webhooks
- Form and transactional email delivery
- Checkout/payment sandbox probes where safe
- Core Web Vitals, response time, cache status, and database growth
- Broken links, indexing directives, sitemap, and unexpected DNS changes

Monitoring must not create orders, send real campaigns, alter records, or expose secrets. Use synthetic/test accounts and sandbox endpoints where possible.

## Maintenance cadence

- **Daily:** uptime, backups, critical errors, checkout/forms/email, security alerts.
- **Weekly:** updates, cron/webhooks, resource trends, spam, broken critical journeys.
- **Monthly:** restore test, user/role review, performance, accessibility/SEO spot checks, dependency and license inventory.
- **Quarterly:** disaster recovery exercise, PHP/WordPress roadmap, data retention, plugin rationalization, full QA.

## Incident runbook

1. Confirm impact and preserve evidence.
2. Stop harmful automation or external side effects only when authorized.
3. Stabilize availability and protect data.
4. Communicate known facts, uncertainty, owner, and next update.
5. Identify root cause after containment.
6. Restore, reconcile, and verify critical journeys.
7. Record corrective and preventive actions.

## Privacy and consent

Inventory data collected by forms, accounts, ecommerce, analytics, embeds, advertising, chat, logs, backups, and integrations. Record purpose, retention, access, deletion/export path, processor, and consent dependency.

Check WordPress personal-data export/erasure tools, form retention, cookies/storage, consent mode, script blocking, third-party embeds, IP/email logging, backups, and webhook payloads. Avoid collecting sensitive data in diagnostic reports.

Provide technical implementation guidance, not legal certification. Ask for jurisdiction and counsel-approved requirements when legal interpretation is required.
