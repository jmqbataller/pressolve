# Real-Estate, IDX, MLS, and RESO

## Establish the data relationship

Before recommending an IDX solution, identify:

- Country, market, brokerage/agent role, and the specific MLS organization
- MLS approval, display, attribution, refresh, retention, and compliance rules
- Vendor/IDX agreements and available WordPress integrations
- Required search, map, saved-search, alert, lead-routing, CRM, and analytics features
- SEO expectations and whether listing pages are indexable/rendered on the site
- Budget, support responsibility, portability, and exit plan

Do not imply that one IDX plugin works with every MLS. Verify vendor coverage and MLS approval using current official sources.

## Architecture options

- **Hosted/iframe search:** Fast to deploy but may limit design, analytics, SEO, and accessibility.
- **Vendor WordPress integration:** Balanced setup with vendor-managed feed and WordPress presentation.
- **API-driven build:** Highest flexibility with greater compliance, infrastructure, caching, and maintenance responsibility.

Explain data ownership, refresh timing, canonical/indexing behavior, lead ownership, vendor lock-in, and migration risk for each option.

## Site structure

Support property search, listing detail, community/neighborhood pages, agent profiles, valuation/contact flows, saved searches, market content, and CRM lead routing. Keep claims and listing data synchronized with the approved source.

## Troubleshooting

For missing or stale listings, trace MLS source status, vendor ingestion, eligibility/display rules, account approval, refresh schedule, filters, cache/CDN, template rendering, and API limits. Preserve listing IDs and timestamps in evidence while redacting client information.

For maps/search, verify geocoding, API restrictions, billing, consent, mobile performance, keyboard interaction, and empty/error states.

## RESO guidance

Explain RESO standards without presenting them as direct database access. Confirm the specific provider's Web API authentication, fields, replication/display permissions, rate limits, media rules, and compliance requirements before designing an integration.
