# Verification record

The current release is generation 5. The canonical journal is `deploy/proof.json`; the read-only audit output is `docs/proof-verifier-output.txt`. The full read-only audit passed: four deployed sources, 32 finalized receipts and real explorer records, five pinned compiler metadata snapshots, three earliest eligible evidence revisions, YES/NO/multiple-choice/rejection, both live markets, the credited 11 wei claim, and the real free prediction with overall/season standings. See `deploy/verification.json`. Production remote build dpl_5S8FzS3SkD9BtQSBq4acNRnjdMC7 completed successfully. All seven routes were captured at both requested viewports after the phone grid correction. See `.impeccable/review/flow-checks.json` and `interactive-checks.json`.

## Executed checks

GenVM lint passed for the four product contracts and both diagnostic sources. Fifty direct contract tests passed across isolated processes: Markets 16, Pools 16, Resolver 13 and Seasons 5. The current compiler's sixteen tests were rerun after the metadata-only repair. Eleven application tests, strict TypeScript and ESLint passed. Local and remote Next.js production builds passed. The final publication includes another remote production build; no local prebuilt output is deployed.

Direct tests mock web and model responses and do not establish multi-validator consensus. They cover compile acceptance/rejection, real saved wikitext extraction, digest and quote mismatch, prompt injection, revision timing, UNCLEAR, missing summaries, VOID, deadline refunds, empty winning sides, payout remainders, duplicate claims and authorization.

## Finalized chain demonstration

The current four-contract deployment has two accepted live War season-one forecasts, three resolved historical rehearsals (YES, NO and multiple choice), and a genuinely rejected subjective question. Historical rehearsals are excluded from competitive scoring. Live calls remain pending until their broadcast and settlement windows.

Compilation selects the latest Wikipedia metadata revision at or before proposal time. Code extracts episode identity, dates and summary-path existence without sending plot bodies to the compiler. An empty future ShortSummary field is a valid path. Validators independently fetch the permanent revision, check its digest, enforce schema and deadlines, and judge the proposed specification. Accepted live cases were run on-chain after the prompt repair. A rejection may omit only `spec: null`; code inserts that null and still rejects unknown keys and malformed accepted specs.

The real application wallet adapter sent a zero-value free prediction from a Node EIP-1193 signer. Its transaction finalized successfully; predictions and overall/season leaderboard rows were read back. `deploy/wallet-adapter-check.json` contains the receipt. This verifies signing and transport through the application's actual `send` function. The owner also connected MetaMask in Chrome and signed a real zero-value prediction for market-2. Activity displayed ACCEPTED with its appeal window, preserved the hash across reload, and then displayed FINALIZED SUCCESS. My predictions fetched the actual YES call from finalized state; explicit score reveal showed PENDING and zero points, and global re-shielding hid personal scores again. `docs/browser-verifier-output.txt` independently verifies the receipt, target, value, personal prediction and explorer record.

## Approved native payout

The owner-approved 11 wei deposit belongs to the preserved previous deployment. Its pool is explicitly identified in `poolDemo.legacyContracts` and the app's Proof panel. The current pool uses identical source; the verifier compares committed and deployed bytes for both implementations. The pool allocated all 11 wei and the account is PAID. Verification requires the claim parent's linked native child to be finalized with `value_credited: true`, the correct recipient, and value 11. No second deposit was made. Rerunning the pool or claim stage exits with completed PAID status.

The previous partial audit verified four sources, 25 receipts/explorer records, three immutable evidence revisions and the credited native claim, then correctly failed its mandatory missing-rejection check. Its log is retained as `docs/proof-verifier-v3-checkpoint.txt`; it is not presented as a full current-release pass.

## Browser evidence

The interface has been exercised at actual 1440×960 and 390×844. Checks include a preselected NO option, responsive frozen specifications and UTC dates, the no-wallet error, disabled zero-amount stake preparation, deposit gating without a finalized ticket, and live lookup of both an accepted and rejected proposal. Console error/warning lists were empty in those checks. The final 14 captures cover Discover, Propose, Predictions, Activity, Proof, live market and historical multiple-choice detail. All have no horizontal overflow. The deployed UI revealed actual YES, NO and Gregor Clegane outcomes, loaded actual overall and War season standings, cleared rows on scope changes, and cleared quotes/definitions/standings through shield controls. A historical live refresh followed by Hide restored the spoiler mask. Console warnings/errors were empty. Wallet-populated personal state, actual extension signing, and reload-safe Activity were subsequently verified in Chrome with an owner-signed free prediction. The Chrome profile emitted installed-wallet extension injection warnings; the application flow completed. The no-extension in-app-browser route matrix had no console warnings/errors.

The initial payload removes historical propositions, definitions, outcomes, evidence and payout data. Global re-shielding clears revealed markets, personal scores and standings; an epoch guard prevents an older in-flight request from restoring revealed content. Recorded proof and live finalized reads are labeled separately.

## Schedule and operational limits

War S1E4 broadcasts October 23, 2026 at 01:00 UTC and first becomes eligible for resolution October 25 at 01:00 UTC. S1E5 broadcasts October 30 at 01:00 UTC and first becomes eligible November 1 at 01:00 UTC. The official monthly schedule and syndicated HBO release support Thursday 9pm Eastern; the official trailer page returned automated HTTP 403. Sources and UTC conversion are preserved in `deploy/schedule-sources.json`. Seeding asserts exact frozen broadcast timestamps.

No natural VOID occurred in the successful historical cases. VOID and refunds are demonstrated in direct tests only; no artificial on-chain VOID is claimed. Wikipedia and StudioNet access can be intermittent. Server RPC budgets are process-local rather than distributed across Vercel instances. The project uses simulated StudioNet GEN. Portal submission remains the owner's action.

## Finish review

The fresh full frontend review requested one material change: concise market-detail headings while preserving the exact immutable question in an expandable field. The follow-up reviewer scored that fix resolved and returned `ship` at the fix-only scope. DESIGN.md and its sidecar were refreshed from the built interface. This design verdict does not certify backend consensus; the independent on-chain audit provides that evidence.

The real MetaMask Activity flow was reloaded after finalized success: its state read-back completed, contained market-2/option 0 in shielded form, and persisted across another reload. Polling now continues after finalized success until this read-back exists, so an interrupted read can resume. The additional regression test checks that finalized errors stop and successful receipts without read-back remain retryable. Populated Activity and personal predictions were also checked at both requested viewport sizes; the phone prediction text occupies a full row above its actions.
