# Build and inspect a spoiler-safe prediction

Plot Armor separates a TV theory into four contracts because judging evidence and accounting for stakes are different jobs. This tutorial follows the actual public methods in `contracts/`, the Next.js routes in `app/`, and the resumable scripts in `scripts/`. It assumes you have installed the pinned dependencies described in the README. You can browse the deployed application without connecting a wallet; connecting is only necessary when signing a prediction, proposal or claim.

## Start with a question

Open Propose a market and enter a concrete question, show, season and episode. A question such as whether a named character dies has an observable answer in an episode summary. A question asking whether an episode is good is subjective and must be rejected. For multiple choice, describe two to six distinct, non-overlapping options in the question. Do not supply your own evidence server or revision ID. Participants never choose the resolution evidence.

The form calls `PlotMarkets.propose(question, show, season, episode)`. Compilation searches Wikipedia, then code selects each candidate article’s latest revision at or before the proposal timestamp. It fetches permanent `oldid` raw wikitext and extracts only infobox fields, cast metadata, episode identity, dates, and the existence of the matching summary field or heading. The model never receives plot bodies during compilation. An existing empty future `ShortSummary` is a valid extraction path. The leader returns a strict JSON specification with an ISO air timestamp. Python converts that timestamp to Unix seconds; the model never performs that conversion. Validators independently select the same fixed metadata revision, fetch its immutable raw content, compare its digest, and reconstruct its metadata view. They also enforce exact schema, entry and resolution deadlines, the rehearsal flag, option bounds and code-verified path before judging whether the complete proposed specification is faithful to the source and question. They verify episode identity, date, options, definitions and the extraction path. This avoids requiring identical prose from independent models while still verifying the substance against independent evidence.

An accepted specification includes its proposition, definitions, options, article, extraction mode, air timestamp and deadlines. Code hashes canonical JSON. The market stays `PENDING_FINALITY` until a self callback emitted on finality makes it `OPEN`. Rejections become `REJECTED` and preserve a reason. The Activity page distinguishes submission, pending consensus, accepted consensus, finalized success and finalized error. It saves hashes in local storage, polls every ten seconds and reads finalized contract state after success. An accepted receipt alone does not mean the appeal window has closed.

## Make a free prediction

Open an accepted market before its entry deadline. Select a listed outcome and choose free points. `PlotSeasons.predict` reads the market and freezes one immutable prediction per wallet. The contract accepts only valid option IDs and timely entries. It records the show-season grouping and the episode's chronological position. Once a result finalizes, anyone can call `score(wallet, market)` for the prediction. Correct live calls earn ten points; incorrect calls earn zero; void calls do not award points. Historical rehearsals never add competitive points. Leaderboards derive streaks in episode order, so submitting score calls in a convenient order cannot manufacture a longer streak.

## Prepare a pool stake

A GEN stake takes two explicit transactions. First call `PlotPools.prepare_stake` with the market ID, selected option and amount in wei. This zero-value method checks the finalized source, deadline, capacity and previous participation. It returns a wallet-bound ticket with a short expiry. After finality, read `get_ticket`, verify its market, wallet, option and exact amount, then call `deposit(ticket)` with that amount.

This split addresses an observed StudioNet behavior: a failed payable call can credit value without applying contract state. A well-formed invalid deposit therefore records a refund credit rather than relying on a revert. A malformed call that truly fails after value is credited can be recovered through `recover_failed_deposit`, which independently checks the finalized protocol receipt and prevents duplicate recovery. The release script does not automatically send deposits. The first owner approval covered eleven wei on a previous deployment. A separate owner instruction authorized exactly 2 simulated GEN on the submitted PlotPools; `scripts/submitted_pool_demo.py` implements that distinct demonstration with durable hashes, finalized state reads and exact balance snapshots.

## Follow settlement evidence

Resolution starts no earlier than forty-eight hours after the frozen air timestamp. `PlotResolver.resolve` asks the Wikipedia revisions API for revisions in ascending order after that threshold. Code fetches candidates and extracts either the individual episode Plot section or the matching Episode list ShortSummary. It scans five candidates per attempt and retains the continuation token only after checking earlier candidates. The first candidate containing a usable summary becomes the permanent evidence revision.

The LLM sees only the extracted summary and frozen specification. It returns one listed option ID or `UNCLEAR`, plus an eight-to-four-hundred-character verbatim passage. Each validator repeats the extraction, checks its digest, makes its own outcome judgment and confirms that the leader's quote occurs in its own summary. A missing quote or digest mismatch cannot pass consensus. Commands embedded in the fetched summary are untrusted content, never instructions.

When evidence is missing or unclear, the market remains retryable. At the resolution deadline it becomes VOID. A caller cannot force a convenient winner. Use `npm run settle` later to resume eligible settlements without redeploying or resubmitting completed stages.

## Claim and verify a payout

Once entries close and the resolver has a finalized outcome, call `PlotPools.settle`. Code allocates the entire pool proportionally among winning stakes. Prefix-based integer allocation distributes remainder wei deterministically. An empty winning side, a void result or a missed resolution deadline instead allocates full refunds. A finality callback exposes the settled pool for claims.

Call `claim(market, attempt)` to emit a native transfer on finality. This parent transaction and the native child have separate receipts. `verify_claim` checks the original claim calldata, attempt, recipient, amount, parent-child relationship, finality and explicit native credit. It marks a claim PAID only when value was credited. An explicit failed credit enables another attempt. A pending or unknown credit never permits duplicate payment.

Finally, run the read-only proof verifier. It compares deployed sources, finalized state, receipts, quote digests and explorer API records. It reads no release secrets and signs nothing. Inspect the actual verification report for results; passing mocks or an HTTP 200 explorer shell cannot replace live proof.


## Compiler resilience and release history

The repaired compiler canonicalizes one harmless model formatting variation: a rejection with `accepted: false` and a reason may omit its null spec. Code inserts `spec: null` before enforcing the exact schema. Unknown keys, a missing decision, a missing reason, and an incomplete accepted specification still fail. This does not change who judges the question: validators independently rerun rejection judgments or verify accepted specifications against their own fetched evidence. Transient Wikipedia HTTP errors receive at most three attempts with the same browser user agent used by the deployed probe. An unaired episode may have an existing episode row whose summary is still empty; its future extraction path is valid without inventing a future plot.

The old 11 wei lifecycle remains previous-deployment history in `previousPoolDemos`. The submitted PlotPools separately completed a newly authorized 2 GEN lifecycle on market-7. Compilation and resolution finalized before its winning-option stake was prepared. Settlement waited for the rehearsal entry cutoff. The native child credited exactly 2 GEN, then `verify_claim` marked the claim PAID. That method updates state directly and emits no extra callback. The wallet returned to 2.000000000000000011 GEN and the submitted pool returned to zero. Neither approval is reused for another deposit.
