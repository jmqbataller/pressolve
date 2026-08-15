# Content Modeling and Migration

## Model before importing

Define post types, taxonomies, users/authors, statuses, dates/timezones, relationships, ACF/meta fields, media, translations, canonical URLs, permissions, and deletion/retention rules. Decide which system owns each field after migration.

Create a mapping table:

| Source field | Destination | Transform | Required | Validation | Fallback |
|---|---|---|---|---|---|

## Import safety

1. Preserve the original export and calculate counts/checksums where practical.
2. Test a small representative batch on staging.
3. Make imports idempotent using stable external IDs.
4. Validate and sanitize data without discarding meaningful formatting.
5. Download media safely, verify MIME/type/size, and preserve attribution/alt text.
6. Record rejected rows and reasons.
7. Avoid duplicate terms, users, media, and posts on retries.
8. Use serialized-safe tools for WordPress data.

## Multilingual content

Map language, translation groups, hreflang, slugs, canonical URLs, media, menus, taxonomies, and fallback behavior. Confirm the target multilingual plugin's supported import API and do not manipulate its internal tables by guesswork.

## Cutover and reconciliation

Plan content freeze or delta import for changing sites. For commerce, memberships, forms, or bookings, separate content migration from live transactional data and reconcile by stable IDs/timestamps.

Create a redirect map for every changed public URL. Verify counts, sampled field values, relationships, media, authors, dates, search, archives, templates, metadata, canonical/indexing rules, redirects, and permissions.

Do not delete the source or temporary mapping data until acceptance and rollback windows close.
