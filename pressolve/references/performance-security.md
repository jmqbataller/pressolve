# Performance and Security

## Performance investigation

Measure before changing configuration. Capture representative mobile and desktop tests, logged-out and logged-in behavior where relevant, geography, cache status, and server timing.

Separate:

- **Frontend:** images, fonts, CSS/JavaScript, third parties, DOM size, layout shifts
- **WordPress/PHP:** slow hooks, plugin work, uncached requests, REST/AJAX, cron
- **Database:** slow queries, autoloaded options, indexes, table growth, locks
- **Infrastructure:** CPU, memory, PHP workers, disk, object cache, network, CDN

For Core Web Vitals, connect the metric to the responsible element or request. Do not promise a score. Re-test multiple times and verify that functionality, analytics, consent, checkout, and authenticated pages remain correct.

## Cache discipline

Map every cache layer before purging or enabling another one: browser, page cache, reverse proxy, CDN, object cache, opcode cache, and application/plugin cache. Prevent overlapping optimization features from performing duplicate minification, delay, or image rewriting.

Exclude personalized, cart, checkout, account, preview, nonce-sensitive, and authenticated responses as required by the application. Verify cache headers and variants rather than relying only on a plugin banner.

## Security baseline

- Keep core, plugins, themes, PHP, and dependencies supported and patched.
- Apply least privilege and remove unused accounts/components.
- Require strong authentication and MFA where supported.
- Protect backups separately and test restoration.
- Disable dashboard file editing where operationally appropriate.
- Limit file types, validate uploads, and restrict execution in upload locations.
- Use TLS, secure cookies, appropriate headers, and trusted update sources.
- Log important admin, authentication, and integration events without collecting secrets.

## Suspected compromise

Do not begin by deleting suspicious files. First confirm scope, preserve logs/evidence, identify the clean recovery point, and coordinate with the host. Contain access, rotate affected credentials from a clean device, replace WordPress/vendor files from trusted sources, inspect persistence mechanisms, patch the entry point, and monitor after recovery.

Clearly distinguish basic triage from a professional incident response or malware-clean certification.
