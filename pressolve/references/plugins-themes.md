# Plugins, Themes, and Templates

## Plugin selection

Define the required capability and check whether WordPress core, the active theme/builder, or an existing plugin already provides it. Evaluate candidates using current official evidence:

- Supported WordPress and PHP versions
- Recent release and maintenance history
- Public support quality and documentation
- Security advisories and remediation status
- Accessibility and localization support
- Performance footprint and background jobs
- Data portability, uninstall behavior, and vendor lock-in
- Licensing limits, renewals, and required add-ons
- Compatibility with caching, multisite, WooCommerce, builders, and hosting

Do not treat install count or star rating as proof of fitness. Recommend a controlled staging test with the real theme, content, and integrations.

## Plugin replacement

1. Inventory settings, stored data, shortcodes, blocks, scheduled jobs, webhooks, and frontend output.
2. Confirm export/import or migration options.
3. Build the replacement on staging without deleting the original data.
4. Test permissions, forms, email, cron, performance, and mobile output.
5. Schedule cutover and rollback.
6. Remove old data only after an agreed retention period and verified backup.

## Update strategy

- Read the changelog and known issues for significant updates.
- Verify minimum PHP/WordPress requirements and deprecated integrations.
- Back up files and database together.
- Update on staging, clear the appropriate caches, and run critical-path tests.
- Avoid simultaneous core, PHP, theme, and large plugin upgrades when isolation is important.
- Document the previous versions and rollback packages.

## Themes and templates

Use the WordPress template hierarchy to identify the actual source of output. Check, in order, block/FSE templates and template parts, builder conditions, child theme overrides, parent theme templates, plugin templates, and custom hooks.

Prefer:

- Site Editor/global styles for block themes
- Builder Theme Builder features for builder-owned templates
- Child themes for parent-theme PHP/template overrides
- A small site-specific plugin for functionality that should survive theme changes

Never edit WordPress core or a vendor-managed parent theme. Before changing templates, capture global styles, display conditions, menus, widget areas, customizer settings, and responsive behavior.

## Broken layout checks

1. Reproduce at exact viewport and user state.
2. Inspect missing/failed CSS, JavaScript, fonts, and images.
3. Check cache/minification and regenerated builder assets.
4. Identify selector specificity, container width, overflow, positioning, and z-index issues.
5. Test logged-in versus logged-out rendering.
6. Verify desktop, tablet, mobile, keyboard focus, and reduced motion.
