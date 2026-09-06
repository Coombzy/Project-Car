import Link from "next/link";

import {
  BAY_KITS,
  BAY_PREFIXES,
  CRIB_PREFIX,
  kitHref,
  type ToolPrefix,
} from "../lib/inventory";

export function InventoryKitNav({ current }: { current: ToolPrefix }) {
  return (
    <div className="inventory-toolbar">
      <div className="view-toggle" role="tablist" aria-label="Tool inventory">
        <Link
          className={`button ghost${current !== CRIB_PREFIX ? " is-active" : ""}`}
          href={kitHref("B1")}
          aria-current={current !== CRIB_PREFIX ? "page" : undefined}
        >
          Bay kits
        </Link>
        <Link
          className={`button ghost${current === CRIB_PREFIX ? " is-active" : ""}`}
          href={kitHref(CRIB_PREFIX)}
          aria-current={current === CRIB_PREFIX ? "page" : undefined}
        >
          Tool crib
        </Link>
      </div>
      {current === CRIB_PREFIX ? null : (
        <div className="view-toggle kit-bay-toggle" role="tablist" aria-label="Bay kit">
          {BAY_PREFIXES.map((bay) => (
            <Link
              key={bay}
              className={`button ghost${current === bay ? " is-active" : ""}`}
              href={kitHref(bay)}
              aria-current={current === bay ? "page" : undefined}
            >
              {bay}
              {BAY_KITS[bay].shopHoist ? " · shop" : ""}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
