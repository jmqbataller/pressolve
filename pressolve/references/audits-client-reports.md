# Audits, QA, and Client Reports

## Audit evidence levels

Label each finding as:

- **Observed:** Directly reproduced or measured.
- **Supported:** Backed by logs, screenshots, or configuration supplied by the user.
- **Inferred:** Likely based on symptoms but not yet verified.
- **Not tested:** Outside available access or evidence.

Never convert an automated warning into a confirmed defect without validation.

## Website Specialist QA

Test representative desktop and mobile widths and, when available, multiple browsers. Cover:

- Homepage, navigation, search, 404, and key landing pages
- Forms, validation, success/error states, storage, and notifications
- Authentication, roles, protected content, and account flows
- Ecommerce or lead-generation critical journeys
- Responsive layout, overflow, images, fonts, and interactive states
- Keyboard navigation, focus, labels, contrast, and reduced motion
- Status codes, redirects, metadata, canonical/indexing rules, and sitemap
- Console/network errors, performance, caching, cron, and integrations
- Backup recency, update status, security basics, and monitoring

Do not submit forms, create orders, send email, alter records, or trigger integrations on production unless authorized. Use clearly labeled test data and clean it up when permitted.

## Prioritization

| Priority | Definition |
|---|---|
| Critical | Active outage, data loss, compromise, payment failure, or severe compliance risk |
| High | Core user journey broken or a likely near-term operational risk |
| Medium | Material performance, SEO, accessibility, maintainability, or UX issue |
| Low | Minor defect or optional improvement |

Include evidence, affected scope, business/user impact, recommended action, risk, owner, and verification for each item.

## Client-ready language

Lead with impact and next action. Translate technical causes without blaming the client or another vendor. Separate confirmed findings from possibilities. Avoid invented time estimates; provide a range only after scope and dependencies are known.

Use this compact structure:

1. Executive summary
2. Completed checks
3. Prioritized findings
4. Recommended action plan
5. Risks, dependencies, and decisions needed
6. Verification or acceptance criteria
