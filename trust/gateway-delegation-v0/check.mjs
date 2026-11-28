#!/usr/bin/env node
/**
 * Second implementation of the gateway-delegation checks, in JavaScript, kept
 * deliberately independent of check.py: same inputs, same published check
 * order, same three-valued outcome. It exists so that one implementation is not
 * the only witness of the other.
 *
 * Usage:
 *   node check.mjs            # curated cases and vectors, JSON on stdout
 *   node check.mjs --vectors  # vectors only
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PASS = "pass";
const FAIL = "fail";
const RECORD = "record-unresolved";   // the record, or what it points at, cannot be resolved
const ABSENT = "absent";              // nothing was declared, so there was nothing to check against
const CHECKER = "check-incomplete";  // the check itself could not be completed

function readJSON(p) {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function parseTime(value) {
  if (typeof value !== "string") throw new Error("not a string");
  let text = value.trim();
  if (!/z$|[+-]\d{2}:?\d{2}$/i.test(text)) text += "Z"; // naive timestamps are UTC, as the policy says
  const ms = Date.parse(text);
  if (Number.isNaN(ms)) throw new Error("unparsable");
  return ms;
}

function listJSON(dir) {
  return fs.readdirSync(dir).filter((f) => f.endsWith(".json")).sort()
    .map((f) => readJSON(path.join(dir, f)));
}

function checkCase(c, policy) {
  const now = parseTime(policy.evaluatedAt);
  const bound = Number(policy.revocationFreshnessBoundSeconds) * 1000;
  const mandate = c.mandate || {};
  const request = c.request || {};
  const payload = request.payload || {};
  const checks = [];
  const add = (name, result, code) => checks.push({ check: name, result, code: code || "" });

  if (request.agentId === mandate.subject) add("subject", PASS);
  else add("subject", FAIL, "SUBJECT_MISMATCH");

  try {
    const issued = parseTime(mandate.issuedAt);
    const expires = parseTime(mandate.expiresAt);
    if (now < issued) add("window", FAIL, "MANDATE_NOT_YET_VALID");
    else if (now >= expires) add("window", FAIL, "MANDATE_EXPIRED");
    else add("window", PASS);
  } catch (e) {
    add("window", CHECKER, "WINDOW_UNPARSABLE");
  }

  if (mandate.signature === "ok") add("signature", PASS);
  else add("signature", FAIL, "MANDATE_UNSIGNED");

  const declared = request.declaredScope || [];
  const granted = mandate.grantedScope || [];
  if (!declared.length) add("attenuation", ABSENT, "NO_DECLARED_SCOPE");
  else if (declared.some((s) => !granted.includes(s))) add("attenuation", FAIL, "SCOPE_WIDENED");
  else add("attenuation", PASS);

  if (payload.opaque) add("content", CHECKER, "OPAQUE_CONTENT");
  else if (payload.instructions) add("content", FAIL, "CONTENT_OVERRIDE");
  else if (payload.claimedRole) add("content", FAIL, "ROLE_SPOOF");
  else add("content", PASS);

  const rev = c.revocation || {};
  const status = rev.status;
  let checked = null;
  try {
    checked = parseTime(rev.checkedAt);
  } catch (e) {
    checked = null;
  }
  if (status === "none") {
    if (checked === null) add("revocation", RECORD, "REVOCATION_UNKNOWN");
    else if (now - checked > bound) add("revocation", RECORD, "STALE_REVOCATION");
    else add("revocation", PASS);
  } else if (status === "revoked") {
    let effective = null;
    try {
      effective = parseTime(rev.effectiveFrom);
    } catch (e) {
      effective = null;
    }
    if (effective !== null && now < effective) add("revocation", RECORD, "REVOCATION_NOT_YET_EFFECTIVE");
    else add("revocation", FAIL, "REVOKED");
  } else if (status === "unreachable") {
    add("revocation", RECORD, "SOURCE_UNREACHABLE");
  } else {
    add("revocation", RECORD, "REVOCATION_UNKNOWN");
  }

  const evidence = c.evidence || {};
  if (evidence.pointer === "reachable") add("evidence", PASS);
  else add("evidence", RECORD, "POINTER_UNREACHABLE");

  const subjectFp = mandate.subjectKeyFingerprint;
  const signerFp = mandate.signatureKeyFingerprint;
  if (!subjectFp && !signerFp) add("signer-binding", CHECKER, "SIGNER_KEY_UNSPECIFIED");
  else if (subjectFp && signerFp && subjectFp === signerFp) add("signer-binding", PASS);
  else add("signer-binding", FAIL, "SIGNER_KEY_NOT_BOUND");

  const lineage = c.lineage;
  if (lineage) {
    const chain = lineage.chain || [];
    if (chain.includes(lineage.predecessor)) add("lineage", PASS);
    else add("lineage", RECORD, "LINEAGE_UNRESOLVED");
  }

  if (checks.some((x) => x.result === FAIL)) {
    const receipt = c.receipt || {};
    if (receipt.decision === "refuse" && receipt.caseId === c.id && receipt.policyDigest === policy.policyDigest) {
      add("receipt", PASS);
    } else {
      add("receipt", FAIL, "RECEIPT_MISSING_ON_REFUSE");
    }
  }

  const results = checks.map((x) => x.result);
  let result = PASS;
  if (results.includes(FAIL)) result = FAIL;
  else if (results.includes(RECORD)) result = RECORD;      // a record we cannot resolve outranks a check we cannot run
  else if (results.includes(ABSENT)) result = ABSENT;       // so does a declaration the record never made
  else if (results.includes(CHECKER)) result = CHECKER;
  const first = checks.find((x) => x.code);
  return {
    id: c.id,
    result,
    decision: policy.decisionMap[result],
    code: first ? first.code : "",
    unknown: {
      record: checks.filter((x) => x.result === RECORD).map((x) => x.code),
      absent: checks.filter((x) => x.result === ABSENT).map((x) => x.code),
      checker: checks.filter((x) => x.result === CHECKER).map((x) => x.code),
    },
    checks,   // per-check detail: same shape as the Python implementation emits
  };
}

const policy = readJSON(path.join(HERE, "policy.json"));
const curated = listJSON(path.join(HERE, "fixtures", "cases"));
const vectors = listJSON(path.join(HERE, "fixtures", "vectors"));
const set = process.argv.includes("--vectors") ? vectors : curated.concat(vectors);
const rows = set.map((c) => checkCase(c, policy));
process.stdout.write(JSON.stringify({ schema: "aikr-gateway-delegation-results/0", impl: "javascript", results: rows }, null, 2) + "\n");
