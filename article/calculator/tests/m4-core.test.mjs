import assert from "node:assert/strict";
import test from "node:test";
import { DEMO_CONFIG, calculateM4, validateConfig } from "../app/lib/m4.ts";

test("demo scenario has a valid lower bound and feasible schedule", () => {
  assert.deepEqual(validateConfig(DEMO_CONFIG), []);
  assert.deepEqual(
    DEMO_CONFIG.taskClasses.map(({ aiCycleMultiplier }) => aiCycleMultiplier),
    [0.76, 0.82, 0.93, 0.87, 1],
  );
  assert.ok(DEMO_CONFIG.taskClasses.every((item) => item.evidence?.url));
  assert.ok(DEMO_CONFIG.taskClasses.every((item) => item.evidence?.publishedAt?.startsWith("2026-")));
  const result = calculateM4(DEMO_CONFIG);
  assert.ok(result.b4 <= result.schedule.makespan);
  assert.ok(result.schedule.makespan < result.tHuman);
  assert.equal(result.demonstratedSpeedup, result.tHuman / result.schedule.makespan);
  assert.equal(result.speedupCeiling, result.tHuman / result.b4);
  assert.ok(result.pSweep.length >= 6);
});

test("unsafe evidence links are rejected", () => {
  const unsafe = structuredClone(DEMO_CONFIG);
  unsafe.taskClasses[0].evidence.url = "javascript:alert(1)";
  assert.match(validateConfig(unsafe).join(" "), /ссылка evidence/i);
});

test("cyclic task graph is rejected", () => {
  const cyclic = structuredClone(DEMO_CONFIG);
  cyclic.tasks[0].predecessors = [cyclic.tasks.at(-1).id];
  assert.match(validateConfig(cyclic).join(" "), /цикл/i);
});
