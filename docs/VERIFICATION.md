# Verification record

The owner-authorized **2 GEN payout is PAID on the submitted PlotPools**, on owner-only historical market-7. No contract source or address was changed and no contract was redeployed. The expanded independent audit passed all 44 finalized receipts and explorer records, all four deployed source matches, six compiler snapshots and four historical evidence checks across three immutable revisions. The exact current-wallet and pool balances also passed. The release is marked submission-ready. The final public link audit passed all 68 distinct URLs: 8 contract records, 45 transaction/API references and 15 other HTTP 200 links, with zero failures. The 45 references comprise 44 canonical transaction pages plus one archived API citation. Explorer API requests used a browser user agent. Full results are in docs/link-audit.json.

## Checks actually run

The follow-up reran all 50 direct contract tests in isolated processes: Markets 16, Pools 16, Resolver 13 and Seasons 5. GenVM lint passed for all four product sources and both diagnostic sources with the pinned runner. Its latest-runner metadata lookup was unavailable, so it used the local runner cache; the requested runner remained pinned. All 12 app tests, TypeScript, ESLint and the updated local production build passed. The additional app test binds the current-pool proof to its amount and market, while retaining the previous-deployment history case.

Direct tests mock web/model responses. VOID/refund remains **test-only** because no market naturally voided; none was manufactured. These tests also cover injection, missing/unclear summaries, digest/quote mismatch, deadlines, refunds, empty winning sides, payout remainders, duplicate claims and authorization.

## Finality and balance procedure

The release wallet initially held 11 wei and the submitted pool held zero. The owner funded exactly 2 simulated GEN. A fresh historical rehearsal was compiled and resolved before preparing its winning-option stake. Every parent and emitted callback finalized successfully, with state read back after each stage. Settlement waited until the rehearsal entry cutoff, 19 October 2026 at 15:22:37 UTC; it did not settle a future War market. The pool's allocation totaled exactly 2 GEN. The claim parent and native child finalized, the child explicitly reported value_credited true, then verify_claim finalized and the account read PAID. That method updates status directly and emits no verification callback; no nonexistent callback is claimed.

The script saves each hash before polling. A polling timeout resumes that same hash; an execution/state mismatch halts the run. No failed write was relabeled or resubmitted. The approved 2 GEN deposit occurred once.

## Proven payout on submitted PlotPools

Owner-approved stake and payout: **2 simulated GEN** (2000000000000000000 wei). Market: market-7. Wallet: 0x92bf935cc375dd667bf49733ebfcf722f9b32105. Final claim status: **PAID**.
Pool: [0xcFC2062bFab042e9885f58c44a2B8e2Ce061e792](https://explorer-studio.genlayer.com/address/0xcFC2062bFab042e9885f58c44a2B8e2Ce061e792).
verify_claim updates verified status directly; it emits no callback

| Finalized stage | Wallet (GEN) | PlotPools (GEN) | Wallet (wei) | PlotPools (wei) |
|---|---:|---:|---:|---:|
| before_stake | 2.000000000000000011 | 0 | 2000000000000000011 | 0 |
| after_deposit | 0.000000000000000011 | 2 | 11 | 2000000000000000000 |
| after_settlement | 0.000000000000000011 | 2 | 11 | 2000000000000000000 |
| after_native_credit | 2.000000000000000011 | 0 | 2000000000000000011 | 0 |
| after_verified_paid | 2.000000000000000011 | 0 | 2000000000000000011 | 0 |

Wallet decrease on deposit and increase on native payout are exactly 2 GEN. The submitted pool returns to its initial native balance.

## New finalized receipts

- [submitted-2gen-funding](https://explorer-studio.genlayer.com/tx/0x76a65c0f392ca694050eadb8bc4856fe36db5d4dc310c643058753b0c7c0b487)
- [submitted-2gen-compile](https://explorer-studio.genlayer.com/tx/0x1f5a429779b34019c31419ecfa2eba3db328b48257ceb0ed8d22204684634f1e)
- [submitted-2gen-compile-child-0](https://explorer-studio.genlayer.com/tx/0x04e28f5dca7ae988fd1c33916a76607ce9e45ba5c8ebfb70eb801fc537e2d92f)
- [submitted-2gen-resolve](https://explorer-studio.genlayer.com/tx/0x5f04eb1952bd7c3814fb3df7a7b4959178e51b334eed8eecd2c62c97ba0e63ba)
- [submitted-2gen-resolve-child-0](https://explorer-studio.genlayer.com/tx/0xbc71f009e1d8b5450ea17b0802b9e1d2f0af0d5de6fa919e42495865e24e0d2a)
- [submitted-2gen-prepare](https://explorer-studio.genlayer.com/tx/0xa43439ddce78b2ff2170a9e6b8090b83d0fb287be2499d70905e63f3e4f3bac7)
- [submitted-2gen-deposit](https://explorer-studio.genlayer.com/tx/0xd30e4ab89eaa6d710096c9c509b6e7798462df303954c3666eeb0615117f7dd8)
- [submitted-2gen-settle](https://explorer-studio.genlayer.com/tx/0x489262bdd3fdb0d24b29adc2fbda5aab4c97f6bba610ea20c6c9804157ba00bd)
- [submitted-2gen-settle-child-0](https://explorer-studio.genlayer.com/tx/0x7d6185ed7d551ee7f5241ede4d29650a1db38e164229f3ea9cc40e47d231209b)
- [submitted-2gen-claim](https://explorer-studio.genlayer.com/tx/0xb5452775429a0e1bbe117502d8b0de362a4b784f9c49987458a8318437f62158)
- [submitted-2gen-claim-child-0](https://explorer-studio.genlayer.com/tx/0x744873cb03b361f0300db38d10a40a49cd7d3cc9898fcab34b1c45bd133cc69e)
- [submitted-2gen-verify](https://explorer-studio.genlayer.com/tx/0x1d7a3f40fdecb6428d7db759eacf1a7c12ce68c3e63e964dc12d505d86f3e43f)

## Previous-deployment history

The old 11 wei payout belongs to pool 0xc5f81c02035Baf552bb55b93e3b6D716A0d84F8B, preserved in previousPoolDemos with legacy-prefixed receipts. It is previous-deployment history, not proof of the submitted PlotPools. The earlier full audit's 32-receipt result and the older partial checkpoint are historical verification scopes. The expanded audit verified the new current-pool paid state and all 44 recorded receipts; its output is in docs/proof-verifier-output.txt.

## Upcoming live settlements

War S1E4 first becomes eligible on **25 October 2026 at 01:00 UTC** (02:00 Lagos). S1E5 first becomes eligible on **1 November 2026 at 01:00 UTC** (02:00 Lagos). These are upcoming live settlements. They were not settled early. npm run settle enforces air time plus 48 hours. The verified official schedule and UTC conversion are preserved in deploy/schedule-sources.json.

## Browser and release evidence

Earlier verification covered all seven original routes at 1440x960 and 390x844, actual MetaMask signing, accepted/appeal-window display, reload persistence, finalized success and state read-back, personal scores and spoiler reset. The current release adds a recorded 2 GEN PAID panel on market-7 and updates Proof to the submitted pool. The updated production app passed all eight routes (including market-7) at 1440x960 and 390x844: 16 checks, no horizontal overflow and no browser warnings/errors. Captures and metrics are in .impeccable/review/submitted-pool. The market-7 panel visibly shows Recorded 2 GEN payout and PAID, with canonical claim and native-transfer links. Contact sheets were visually inspected. A production live-finalized market refresh, result reveal and spoiler-shield reset also passed. Recorded proof is labeled separately from live finalized reads.

## Operational limits

StudioNet uses simulated GEN. Wikipedia and RPC access can be intermittent; server read budgets are process-local rather than distributed. Future live outcomes and competitive scores remain pending until eligibility and sufficient evidence. No natural VOID has occurred. The Portal draft is prepared for the owner; it has not been submitted.
