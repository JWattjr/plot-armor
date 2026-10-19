# Verification record

Release verification is in progress. This release is not marked submission-ready.

Executed checks: genvm-lint on the four product sources and both diagnostic sources; 44 direct contract tests across isolated processes (the compiler repair reran its ten tests); nine application logic tests; strict TypeScript; ESLint; local and remote Next.js production builds. Direct tests mock web and model responses and do not establish multi-validator consensus. The repaired compiler and final proof panel still require the final production release and browser capture.

## Completed previous-release audit

The read-only checkpoint audit verified four deployed sources against their source commit, 25 finalized successful receipts and real explorer transaction records, and three immutable Wikipedia revisions. It independently scanned ascending revisions to establish the earliest eligible summary, extracted the actual summary, checked its digest, and found the verbatim evidence quote. YES, NO and multiple-choice outcomes were finalized. It also verified conservation of the 11 wei pool and the PAID account with an explicitly credited native child linked to its claim parent. The audit deliberately retained all required release checks and stopped at the missing subjective rejection. It is a partial checkpoint audit, not a full pass. See `deploy/checkpoints/historical-and-payout-verification.json` and `docs/proof-verifier-output.txt`.

The owner-approved 11 wei deposit and payout belong to that preserved deployment. `poolDemo.legacyContracts` identifies it explicitly. The repaired release uses identical pool source; its verifier checks the archived implementation against its committed and deployed bytes. No second deposit is authorized or made. Rerunning `pool` or `claim` exits with the completed PAID status.

## Compiler repair

A separate zero-value diagnostic exposed the malformed model response: a genuine rejection contained `accepted: false` and a reason but omitted `spec: null`. `docs/compile-diagnostic-output.json` records the actual output. The repaired compiler inserts only that missing null, then enforces the exact schema. Unknown fields and incomplete accepted specs still fail. Wikipedia requests use the access-proven browser user agent with three bounded attempts for transient HTTP errors. An existing unaired episode row may have an empty future summary. The positive historical compile is being rerun on-chain after the prompt change; no mock-only success is presented as consensus proof.

The original access probe finalized HTTP 200 for both the Wikipedia revisions API and permanent oldid raw content. A fresh search probe also finalized HTTP 200. Access remains intermittent: some compile attempts receive non-200 discovery responses despite successful probes. Those attempts remain recorded as failed execution, never as rejected proposals.

## Browser and UI review

Ten captures cover Discover, Propose, Predictions, Activity and Proof at actual 1280 by 720 and 390 by 844 viewports. None had horizontal overflow. The fresh finish reviewer scored four corrections resolved: compact honest empty notice, concise shelf questions, removal of ornamental heading eyebrows, and truthful shield state with a mobile reset. This verdict covers those fixes, not backend readiness. The documented system is DESIGN.md and .impeccable/design.json.

Browser interactions confirmed the proposal no-wallet error, historical market choices, explicit result and exact frozen-proposition reveal, live finalized refresh, and global re-shielding on desktop and phone. The initial payload excludes historical proposition text that can itself disclose a winner. Actual YES and multiple-choice evidence appeared only after reveal. Captured console error/warning lists were empty.

The viewport capability accepted 1440 by 960 but left the existing tab at 390 by 844 and a new tab at 1280 by 720. The exact requested desktop matrix is unverified. Browser-extension popup signing is untested. A real Node EIP-1193 adapter check remains planned after an accepted live market; its eventual scope must be distinguished from an extension popup.

## Remaining release proof and limits

No natural VOID occurred in the successful historical cases. Unclear and missing summaries, resolution deadlines, void refunds, empty winning sides and payout remainders are covered by direct tests. No artificial on-chain VOID is claimed.

The official HBO monthly release confirms the premiere date. Its official series press page returned automated HTTP 403; an accessible syndicated press release supplies the Thursday 9pm Eastern schedule. Candidate episode broadcasts are October 23 and 30 at 01:00 UTC, with earliest settlements October 25 and November 1 at 01:00 UTC. The seed now asserts exact frozen broadcast timestamps against that schedule. These are candidates until their on-chain compile accepts.

The repaired four-contract deployment and historical/rejection/live judgments are being rerun. Full current-release proof verification, an accepted live free prediction, final deployment and final captures remain pending. The server RPC budget is process-local, not distributed across Vercel instances. Portal submission is intentionally left to the owner.
