# Pressolve Update Guard

## Scope the change

Record the current and proposed WordPress, PHP, database, theme, builder, plugin, WooCommerce, and integration versions. Identify production criticality, maintenance window, backup recency, staging parity, license access, and rollback packages.

Verify current requirements and changelogs through official sources. Check:

- Minimum/maximum WordPress and PHP support
- Deprecated or removed APIs
- Database migrations and irreversible data changes
- Template override versions
- Block editor, REST, cron, and CLI behavior
- WooCommerce HPOS, checkout blocks, Action Scheduler, subscriptions, and gateway compatibility
- Multisite/network activation behavior
- Cache/CDN, security, multilingual, membership, and builder compatibility
- Vendor-reported known issues and security advisories

## Compatibility matrix

Use columns:

| Component | Current | Target | Evidence | Risk | Required test | Rollback |
|---|---|---|---|---|---|---|

Use one decision:

- **Safe to test on staging**
- **Blocked by missing evidence**
- **Blocked by compatibility**
- **Manual review required**
- **Ready for controlled production update**

Never label an update production-safe from version numbers alone.

## Update sequence

1. Preserve current packages/configuration and verify a restorable backup.
2. Refresh staging and prevent live email, payments, webhooks, search indexing, and analytics side effects.
3. Establish baseline screenshots, logs, performance, and critical journeys.
4. Apply the smallest isolatable change.
5. Run database migrations once and record them.
6. Clear only required cache layers.
7. Test admin/editor, frontend, roles, forms, cron, REST, integrations, and business-critical flows.
8. Compare baseline and post-update evidence.
9. Approve production only with explicit acceptance criteria and rollback trigger.

Avoid combining PHP, WordPress core, database, theme, and major plugin upgrades when root-cause isolation matters.

For PHP changes, capture PHP-FPM/runtime version, loaded extensions, limits, worker saturation, and opcode-cache state before and after the switch. Reset opcode cache through the host's supported procedure, then verify that every worker serves the intended version. Define a containment threshold before starting—for example, any new checkout 500, payment/order mismatch, fatal error, or sustained critical-queue growth triggers immediate rollback to the verified runtime or artifact.

## Rollback limits

File rollback may not reverse database migrations, order/subscription changes, new content, or remote integration side effects. State what is reversible, what requires database restoration, and what data would be lost. For high-change sites, plan a content/order reconciliation strategy rather than assuming a full database rollback is safe. Before retrying a payment or restoring an ecommerce database, reconcile WordPress/WooCommerce order records with the payment provider and external fulfillment systems to avoid duplicate charges or lost orders.
