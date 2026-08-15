# Pressolve

**Pressolve** is an AI WordPress Website Specialist skill for ChatGPT and Codex. It helps users understand WordPress concerns, diagnose failures, choose plugins and themes, implement safe fixes, and verify the result.

> Diagnose. Fix. Build. Optimize.

## Download

[**Download the latest Pressolve ZIP**](https://github.com/jmqbataller/pressolve/releases/latest/download/Pressolve-ChatGPT-Skill-v1.0.0.zip)

The ZIP contains only the installable `pressolve` skill folder. Release assets also include a SHA-256 checksum.

## Use Pressolve

Install or import the downloaded ZIP in a ChatGPT or Codex environment that supports skills, then invoke it with:

```text
$pressolve

My Elementor editor keeps loading after I installed a caching plugin.
The public site still works. Help me diagnose it without downtime.
```

Pressolve may also activate automatically for WordPress troubleshooting and Website Specialist requests when implicit skill invocation is supported.

## Core capabilities

- WordPress how-to instructions and dashboard guidance
- Screenshot, error-message, log, and code diagnosis
- Plugin selection, comparison, conflicts, replacement, and updates
- Themes, templates, child themes, Gutenberg, Elementor, Bricks, and Divi
- WooCommerce checkout, gateway, shipping, order, and performance troubleshooting
- Core Web Vitals, caching, database, PHP, and hosting performance
- Security hardening, backup planning, recovery, and compromise triage
- DNS, SSL, CDN, SMTP, migrations, deployment, and WP-CLI
- PHP, hooks, REST API, AJAX, JavaScript, CSS, ACF, and custom plugins
- Technical SEO and accessibility reviews
- Real-estate IDX, MLS, RESO, property search, and lead-capture guidance
- Website audits, QA checklists, maintenance notes, and client-ready reports

## Safety principles

Pressolve separates observed evidence from inference, prioritizes the least invasive test, requires rollback planning for risky work, and never claims it inspected or fixed a site without the necessary evidence or authorized access.

It does not recommend nulled software, license bypasses, edits to WordPress core, unverified compatibility claims, or destructive production changes without confirmation and backups.

## Diagnostic response format

1. Problem summary
2. Most likely cause and confidence
3. Safest first test
4. Fix steps
5. Rollback
6. Verification
7. Next step if unresolved

## Repository structure

```text
pressolve/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── audits-client-reports.md
    ├── builders-commerce.md
    ├── custom-development.md
    ├── hosting-deployment.md
    ├── performance-security.md
    ├── plugins-themes.md
    ├── real-estate.md
    ├── seo-accessibility.md
    └── troubleshooting.md
```

Repository-level packaging and release files are intentionally kept outside the installable skill folder.

## Build the ZIP locally

```bash
python3 scripts/package.py
```

This creates a deterministic ZIP and checksum in `dist/`.

## Version

Current release: **v1.0.0**

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Author

Developed by [John Mark Bataller](https://jmqbataller.vercel.app/).

## License

[MIT](LICENSE)
