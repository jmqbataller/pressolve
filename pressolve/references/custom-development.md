# Custom WordPress Development

## Architecture choices

- Put presentation overrides in a child theme.
- Put durable site functionality in a site-specific plugin.
- Prefer WordPress core APIs, hooks, blocks, and documented extension points.
- Namespace functions/classes and avoid global collisions.
- Make install, activation, deactivation, upgrade, and uninstall behavior explicit.
- Preserve data by default on uninstall unless deletion is a deliberate, confirmed feature.

## PHP checklist

- Verify capabilities for privileged actions.
- Use and verify nonces for state-changing browser requests.
- Sanitize according to expected input, validate domain rules, and escape at output.
- Use `$wpdb->prepare()` and core query APIs; avoid interpolated SQL.
- Avoid unserializing untrusted data and dynamic file inclusion.
- Handle failures without exposing stack traces, paths, or secrets.
- Make cron, webhook, and retry operations idempotent.
- Consider multisite, localization, timezone, and HPOS when relevant.

## REST, AJAX, and integrations

Define authentication, authorization, schema validation, rate limits, timeouts, retry/backoff, idempotency, logging, and secret storage. For REST routes, always provide a meaningful `permission_callback`. For webhooks, verify signatures and protect against replay where the provider supports it.

Do not place private API keys in browser JavaScript, public repositories, rendered HTML, or `NEXT_PUBLIC`-style variables.

## Frontend code

Enqueue scripts and styles with dependencies and versions. Prefer progressive enhancement, semantic HTML, keyboard support, focus visibility, reduced-motion behavior, and scoped selectors. Avoid broad CSS fixes that hide overflow or focus indicators without correcting the underlying layout.

## Snippet delivery

For every code change state:

1. Purpose and compatibility assumptions
2. Exact file/plugin placement
3. Complete code with comments only where useful
4. Backup and staging requirements
5. Static/lint/runtime checks performed
6. Test cases and expected result
7. Removal or rollback procedure

Review surrounding code before modifying an existing file. Preserve user changes and established project conventions.
