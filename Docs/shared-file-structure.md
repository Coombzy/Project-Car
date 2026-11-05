# Shared File Structure for Apps and Websites

**Date:** 2026-11-04  
**Status:** Proposed for Cortana / Lead review  
**Goal:** One consistent shape for ad assets, catalog data, metrics, and related files so Project Car, pBay, and Liquid Estate can share code and data without duplication.

## Principles

- Single source of truth for ad data lives in the core (pBay as API/data custodian, or the extracted shared service).
- Front-ends (websites and apps) read; they do not keep separate full copies of photos or ad records.
- Data is partitioned by business on disk (`project-car/` and `liquid-estate/` or equivalent).
- Same folder shape and naming everywhere so scripts and agents can treat them uniformly.

## Home-lab / storage layout (canonical)

```
/home-lab/
├── project-car/
│   ├── ads/
│   │   └── {ad-id}/
│   │       ├── photos/
│   │       ├── metadata.json
│   │       ├── listing.json
│   │       └── metrics.ndjson
│   ├── catalog/
│   └── crm/
└── liquid-estate/
    ├── ads/
    │   └── {ad-id}/
    │       ├── photos/
    │       ├── metadata.json
    │       ├── listing.json
    │       └── metrics.ndjson
    └── catalog/
```

- `{ad-id}` is stable and shared across eBay and the direct website.
- `photos/` holds the canonical images (same names and order everywhere).
- `metadata.json` — product facts, condition, dimensions, etc.
- `listing.json` — title, description, price, category, channel-specific fields.
- `metrics.ndjson` — append-only analytics for that ad (views, offers, sales, etc.).

## Repo / code structure (shared shape)

```
apps/
├── shared/                  # extracted core or shared package
│   ├── catalog/
│   ├── ads/
│   ├── pricing/
│   └── types/
├── project-car/
│   ├── api/               # thin adapters or remaining Python
│   └── web/
├── pbay/                   # current Liquid Estate employee app + future core
│   ├── api/
│   └── web/
└── liquid-estate-web/      # thin public site
    └── web/
```

- Shared types and domain logic live under `apps/shared/` (or a published package) once extracted.
- Each app keeps its own thin front-end and any business-specific routes.
- Websites consume the same catalog/checkout API surface.

## Naming conventions (align with agent-scripts where useful)

- Lowercase, hyphen-separated directories.
- Stable IDs for ads and catalog items.
- Metrics files are append-only `.ndjson`.
- Photos use consistent naming (`01.jpg`, `02.jpg`, …) so order is preserved.

## Adoption notes

- Can be adopted incrementally. New ads follow the shape immediately.
- Existing ads can be migrated in batches.
- Front-ends never store a second full copy of photos or ad records; they reference the core.
- This structure works whether the core stays inside pBay or is later extracted.

## Relationship to language plan

The shared file structure is language-agnostic and can be used before the TypeScript convergence is finished. Once the core is TypeScript, the same folder shape is simply served by TS services.

---

*Companion document: `Docs/language-unification-plan.md`*
