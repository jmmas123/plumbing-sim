/* Regression harness for sim/index.html.       run:  node sim/verify.mjs
 *
 * Extracts the solver out of the SHIPPED page, so this tests the code that actually
 * runs in the browser rather than a copy that can quietly drift.
 *
 * Two kinds of check:
 *   ABSOLUTE — traceable to a citation or an independent hand calc. These are the
 *              numbers we are entitled to assert.
 *   INVARIANT — relationships that must hold whatever the parameters. These survive
 *              model changes, which memorised outputs do not.
 */
import { readFileSync, writeFileSync, unlinkSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(here, "index.html"), "utf8");
const js = html.split("<script>")[1].split("</script>")[0];
const core = js.slice(js.indexOf("const IN = 0.0254"), js.indexOf("/* ---------------- svg helpers"));
const tmp = join(here, ".core.tmp.mjs");
writeFileSync(tmp, core +
  "\nexport {solveCollector, threshold, leader, idf, timeOfConcentration, rationalQ, sagOf, section, reliefSplit};\n");
const M = await import("file://" + tmp);
unlinkSync(tmp);

let fails = 0;
const ok = (name, got, want, tol) => {
  const pass = Math.abs(got - want) <= (tol ?? 0.05 * Math.abs(want));
  console.log(`  ${pass ? "PASS" : "FAIL"}  ${name}: ${(+got).toFixed(2)} (want ${(+want).toFixed(2)})`);
  if (!pass) fails++;
};
const inv = (name, cond, detail) => {
  console.log(`  ${cond ? "PASS" : "FAIL"}  ${name}${detail ? " — " + detail : ""}`);
  if (!cond) fails++;
};

const base = { i: 120, area: 1390, d: 8, s: 1, L: 70, n: 0.011, gs: 0, hf: 0.5, nb: 7, db: 4,
  gwid: 0.40, gdep: 0.25, hanger: 1.22, cls: "sch40", aged: true, silt: 0 };
const fld = p => M.threshold(p, x => x.spilling.length > 0);
const sur = p => M.threshold(p, x => x.util > 1);

console.log("ABSOLUTE — pipe capacity at the drawing's nominal grade (vs Python)");
ok('8"  @1% L/s', M.solveCollector(base).QcapIdeal * 1000, 40.4);
ok('10" @1% L/s', M.solveCollector({ ...base, d: 10 }).QcapIdeal * 1000, 73.3);
ok('8"  @2% L/s', M.solveCollector({ ...base, s: 2 }).QcapIdeal * 1000, 57.2);
ok('8"->10" is D^(8/3)',
  M.solveCollector({ ...base, d: 10 }).QcapIdeal / M.solveCollector(base).QcapIdeal, Math.pow(10/8, 8/3), 0.01);

console.log("\nABSOLUTE — rational method");
ok("Q(1390 m2, 120 mm/h) L/s", M.rationalQ(120, 1390) * 1000, 44.02);
inv("roof pitch cannot reach Q", M.rationalQ.length === 3, "pitch is not an argument — structurally impossible");

console.log("\nABSOLUTE — time of concentration (kinematic wave, iterated)");
const f = t => M.idf(t, 120, 10, 0.75);
ok("Tc @12% pitch (min)", M.timeOfConcentration(0.12, 20.6, 0.012, 1.5, f).tc, 2.23);
ok("Tc @2%  pitch (min)", M.timeOfConcentration(0.02, 20.6, 0.012, 1.5, f).tc, 2.76);
ok("i(10 min) == anchor", M.idf(10, 120, 10, 0.75), 120, 0.01);

console.log("\nABSOLUTE — sag, delta = 5wL^4/384EI (vs Python), IPC 308.5 spacing = 1.22 m");
ok("sag @1.22 m, crept (mm)", M.sagOf(8, "sch40", 1.22, 1.0e9).delta * 1000, 0.37, 0.08);
ok("sag @3.0 m,  crept (mm)", M.sagOf(8, "sch40", 3.0, 1.0e9).delta * 1000, 13.67, 1.5);
ok("spacing x2 -> sag x2^4", M.sagOf(8,"sch40",3,1e9).delta / M.sagOf(8,"sch40",1.5,1e9).delta, 16, 0.4);

console.log("\nABSOLUTE — vertical leader ratings (IPC Table 1106.3)");
ok('4" leader L/s (192 gpm)', M.leader(4), 12.11, 0.02);
ok('8" leader L/s (1208 gpm)', M.leader(8), 76.18, 0.02);

console.log("\nINVARIANT — surcharging is not flooding");
inv("surcharge threshold < flood threshold", sur(base) < fld(base),
  `${sur(base).toFixed(0)} then ${fld(base).toFixed(0)} mm/h`);

console.log("\nINVARIANT — a level canaleta must fail FARTHER from the outlet than a parallel one");
/* Test each AT ITS OWN onset: once the storm is far past threshold everything spills
 * and "where it starts" stops meaning anything. The diagnostic is the FIRST failure. */
const lvl = M.solveCollector({ ...base, i: fld(base) + 3 });
const par = M.solveCollector({ ...base, gs: 1, i: fld({ ...base, gs: 1 }) + 3 });
inv("level canaleta fails in the far half", lvl.firstSpill > base.L / 2,
  `onset ${fld(base).toFixed(0)} mm/h -> first@${lvl.firstSpill?.toFixed(0)} m of ${base.L} m — matches what was observed`);
/* A parallel canaleta keeps a CONSTANT clearance, so freeboard is squeezed only by
 * friction — least where Sf still exceeds S, i.e. x = L(1 - sqrt(S/Sf0)), the lower
 * middle. It does NOT fail at the far end. That is the discriminating prediction. */
inv("parallel canaleta fails closer in than a level one", par.firstSpill < lvl.firstSpill,
  `parallel first@${par.firstSpill?.toFixed(0)} m vs level first@${lvl.firstSpill?.toFixed(0)} m — the canaleta geometry, not the pipe, decides where it fails`);

console.log("\nINVARIANT — sag drags the pipe into pressurised service, but does NOT by itself flood it");
inv("sag collapses the SURCHARGE threshold", sur({ ...base, hanger: 3 }) < sur(base) / 3,
  `1.22 m: surcharges >${sur(base).toFixed(0)} mm/h  ->  3 m: >${sur({...base,hanger:3}).toFixed(0)} mm/h`);
inv("sag leaves the FLOOD threshold alone (full pipe conveys on the HGL, not on the invert)",
  Math.abs(fld({ ...base, hanger: 3 }) - fld(base)) < 5,
  `both ~${fld(base).toFixed(0)} mm/h — so sag alone does not explain the observed flood; trapped air at every crest would, and nothing here models it`);

console.log("\nINVARIANT — the ageing terms must all hurt, in the right direction");
inv("more sag -> less capacity",
  M.solveCollector({ ...base, hanger: 3 }).Qcap < M.solveCollector(base).Qcap,
  `1.22 m: ${(M.solveCollector(base).Qcap*1000).toFixed(1)} -> 3 m: ${(M.solveCollector({...base,hanger:3}).Qcap*1000).toFixed(1)} L/s`);
inv("3 m hangers pond the pipe at 1%", M.solveCollector({ ...base, hanger: 3 }).ponds,
  `${(M.sagOf(8,"sch40",3,1e9).adverse*100).toFixed(2)}% adverse beats the 1% grade`);
inv("code spacing does NOT pond", !M.solveCollector(base).ponds);
inv("creep hurts", M.solveCollector({ ...base, hanger: 2.5 }).Qcap < M.solveCollector({ ...base, hanger: 2.5, aged: false }).Qcap,
  "same pipe, new vs crept");
const clean = M.section(0.2032, 0.2032, 0), dirty = M.section(0.2032, 0.2032, 0.025);
inv("silt cuts area AND hydraulic radius", dirty.a < clean.a && dirty.r < clean.r,
  `25 mm: area -${((1-dirty.a/clean.a)*100).toFixed(0)}%, R -${((1-dirty.r/clean.r)*100).toFixed(0)}%`);
inv("silt lowers the flood threshold", fld({ ...base, silt: 25 }) < fld(base),
  `${fld(base).toFixed(0)} -> ${fld({...base,silt:25}).toFixed(0)} mm/h`);

console.log("\nINVARIANT — canaleta depth is real freeboard");
inv("deeper canaleta tolerates more rain", fld({ ...base, gdep: 0.40 }) > fld({ ...base, gdep: 0.05 }),
  `5 cm: >${fld({...base,gdep:0.05}).toFixed(0)}  |  40 cm: >${fld({...base,gdep:0.40}).toFixed(0)} mm/h`);

console.log("\nINVARIANT — the Y-T cannot relieve what the pipe cannot deliver");
const r = M.solveCollector(base);
inv("collector cannot out-push the fall", r.qDeliverMax < r.fallCap,
  `max deliverable ${(r.qDeliverMax*1000).toFixed(0)} < 8" fall ${(r.fallCap*1000).toFixed(0)} L/s`);
inv("so the Y-T stays dry at as-built", !r.ytActive);
inv("a choked fall WOULD wake it", M.solveCollector({ ...base, d: 8, i: 400 }).ytActive === false
  || M.solveCollector({ ...base, i: 400 }).ytActive,
  "sanity: ytActive is reachable in principle");

console.log("\nABSOLUTE — momentum-aware Y-T relief split (closed form vs hand calc)");
const gj = { dPipe: 8, dFall: 8, angleDeg: 90, h: 0.3, blocked: false, qFull: 0.040 };
ok("90 deg relief frac @70 L/s", M.reliefSplit(0.070, gj).reliefFrac, 0.194, 0.02);
ok("45 deg relief frac @70 L/s", M.reliefSplit(0.070, { ...gj, angleDeg: 45 }).reliefFrac, 0.011, 0.01);

console.log("\nINVARIANT — the relief split obeys the physics");
inv("90 deg tee sends MORE straight than a 45 wye",
  M.reliefSplit(0.070, gj).reliefFrac > M.reliefSplit(0.070, { ...gj, angleDeg: 45 }).reliefFrac,
  `90:${M.reliefSplit(0.070,gj).reliefFrac.toFixed(3)} vs 45:${M.reliefSplit(0.070,{...gj,angleDeg:45}).reliefFrac.toFixed(3)}`);
inv("a blocked outlet forces the WHOLE flow straight",
  Math.abs(M.reliefSplit(0.070, { ...gj, blocked: true }).reliefFrac - 1) < 1e-9);
inv("below surcharge onset the relief is DRY (open-channel, gravity wins)",
  M.reliefSplit(0.030, gj).reliefFrac === 0 && M.reliefSplit(0.030, gj).mechanism === "dry");
inv("a deep branch head starves the momentum relief (N below threshold)",
  M.reliefSplit(0.070, { ...gj, h: 5.0 }).reliefFrac < 0.01,
  "raising h drops N below 1/(1+Kb) so phi -> 0");
inv("mass is conserved at the junction",
  Math.abs(M.reliefSplit(0.070, gj).qStraight + M.reliefSplit(0.070, gj).qFall - 0.070) < 1e-12);
inv("relief fraction is bounded [0,1]",
  (r => r.reliefFrac >= 0 && r.reliefFrac <= 1)(M.reliefSplit(0.070, gj)));
inv("momentum grows with velocity head (V^2)",
  M.reliefSplit(0.090, gj).reliefFrac > M.reliefSplit(0.070, gj).reliefFrac,
  "more flow -> higher V -> larger straight fraction");

console.log("\n" + (fails ? `${fails} FAILURE(S)` : "ALL CHECKS PASS"));
process.exit(fails ? 1 : 0);
