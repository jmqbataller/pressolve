# Pressolve Block Studio

## Modern WordPress scope

Support block themes, `theme.json`, Site Editor templates/parts, global styles, custom blocks, dynamic blocks, patterns, synced patterns, block styles/variations, bindings, hooks, components, server-side rendering, and the Interactivity API.

Verify behavior against the target WordPress version because block APIs and editor interfaces evolve quickly.

## Choose the extension point

- Use `theme.json` for design tokens, settings, styles, and editor/frontend alignment.
- Use patterns for reusable editorial compositions.
- Use block variations/styles for controlled variants of an existing block.
- Use block bindings for supported external/meta data connections.
- Use block hooks for automatic placement only when placement remains understandable and removable.
- Build a custom block when semantics, editing controls, saved markup, or behavior require it.
- Use a dynamic block when output must be generated from current server data.

Avoid custom blocks that duplicate stable core blocks with only cosmetic differences.

## Development checklist

1. Define attributes/schema and deprecation/migration behavior.
2. Keep editor and frontend output consistent.
3. Validate capabilities, nonces, REST schemas, and server rendering.
4. Use WordPress packages/components and enqueue dependencies correctly.
5. Provide keyboard behavior, labels, focus handling, reduced motion, and high-contrast states.
6. Test serialization, copy/paste, reusable/synced patterns, revisions, localization, and responsive output.
7. Test activation/deactivation and missing-plugin fallback.

## Interactivity API

Prefer the core Interactivity API for interactive block behavior when it fits the target version. Model global state, local context, derived state, actions, and side effects deliberately. Keep server-rendered markup usable before hydration and avoid storing secrets or privileged decisions in browser state.

## Theme and builder coexistence

Identify whether the Site Editor, a classic theme, or a page builder owns each template. Do not edit the same header/footer/template through competing systems. Document migration boundaries and prevent global styles from unexpectedly overriding builder content.
