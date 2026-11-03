import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { PRIMARY_CAMERA_ID, SAMPLE_CAMERAS, primaryCamera } from "./placeholders.ts";

describe("primaryCamera", () => {
  it("test_primary_camera_is_the_primary_id", () => {
    const camera = primaryCamera();
    assert.equal(camera.id, PRIMARY_CAMERA_ID);
    assert.equal(camera.primary, true);
  });

  it("test_all_sample_camera_ids_are_unique", () => {
    const ids = SAMPLE_CAMERAS.map((c) => c.id);
    assert.equal(new Set(ids).size, ids.length);
  });
});
