# Pressolve v2.1.0

Pressolve 2.1 adds Live Site Audit: paste a WordPress website URL into ChatGPT and Pressolve can begin a bounded, read-only public status review without asking for login credentials.

## Live Site Audit

- Checks redirects, HTTPS, certificate state, public response status, representative pages, robots, sitemaps, REST discovery, metadata, headings, image alt attributes, mixed content, and cache/security-header signals.
- Reviews mobile/desktop rendering, browser console or network errors, accessibility, SEO, and synthetic performance when the available tools support them.
- Detects WordPress and public plugin/theme asset clues with confidence labels and strict warnings against treating clues as a complete inventory or vulnerability result.
- Blocks private/local network targets, validates redirects, respects crawl limits and `robots.txt`, skips sensitive paths, never logs in, and never submits forms, carts, checkout, or other data-changing actions.
- Separates findings visible from a public URL from deeper checks requiring the Connector, WordPress admin, hosting logs, field analytics, or business-system reconciliation.

## Example

```text
$pressolve

Check the whole public status of https://example.com and tell me the Critical,
High, Medium, and Low findings. Clearly identify everything not tested.
```

## Release assets

- `Pressolve-ChatGPT-Skill-v2.1.0.zip`
- `Pressolve-ChatGPT-Skill-v2.1.0.zip.sha256`
- `Pressolve-Connector-v2.1.0.zip`
- `Pressolve-Connector-v2.1.0.zip.sha256`
