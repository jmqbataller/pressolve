# Page Builders, Forms, and WooCommerce

## Builder workflow

Support Gutenberg, Elementor, Bricks, and Divi as primary builders. For other builders, verify current vendor documentation before giving product-specific steps.

Diagnose builder concerns in this order:

1. Template/display condition and content assignment
2. Global design tokens and inherited styles
3. Responsive breakpoint and container/grid configuration
4. Dynamic-data source and permissions
5. Failed REST/AJAX requests or JavaScript errors
6. Generated CSS/cache/minification
7. Theme/plugin conflict or PHP resource limit

Avoid mixing multiple builders on the same template unless there is a documented migration plan. Prefer global styles, reusable components, and semantic structure over per-widget overrides.

## Forms

Verify the entire path: client validation, server acceptance, spam controls, database storage, notification generation, provider acceptance, DNS authentication, and final delivery. Do not assume a successful form message proves email delivery.

Check consent, retention, file-upload restrictions, personally identifiable information, webhook authentication, and retry behavior.

## WooCommerce safety

Treat product, inventory, tax, shipping, checkout, payment, subscription, and order changes as business-critical. Use staging with sandbox gateways where possible, but remember that copied production webhooks and email can create side effects.

For checkout problems, trace:

1. Browser console and checkout network requests
2. WooCommerce status logs and fatal errors
3. Cart/session and cache exclusions
4. Shipping/tax address and zone matching
5. Gateway availability rules and provider logs
6. Theme template overrides and checkout-block compatibility
7. Webhooks, Action Scheduler, stock, and order notes

Never modify live orders, issue refunds, resend customer email, run overdue cron/Scheduled Actions, or trigger payment actions without explicit authorization. Queued jobs may charge renewals, modify orders, send email, or call webhooks. Before retrying any failed-looking payment, reconcile the WooCommerce order, gateway transaction, webhook, and order notes to prevent duplicate charges. Redact customer and payment data.

## WooCommerce customization

Prefer documented hooks, blocks/extensions, and child-theme templates. Record the WooCommerce template version when overriding a template and monitor it after updates. For code, include capability, nonce, sanitization, escaping, idempotency, and HPOS compatibility considerations where relevant.
