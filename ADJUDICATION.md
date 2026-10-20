# Adjudication queue — CrossSource v0.3 (round 1)

**30 items: 17 disagreements, then a seeded random 10% (13) of the 133 agreed items.** For each, read the passage and both raters' reasons, apply [LABELING_PROTOCOL.md](LABELING_PROTOCOL.md) §3 as written, tick the box and write the final label.
- The recommended label and its one-line justification are the curator-model's suggestion. They are not binding.
- Per §7, you may choose A, B or a third label. If the protocol cannot decide an item, drop it rather than force a label.
- If more than 1 of the 13 audit items is wrong, re-label that whole type.

When done, record final labels in `data/v0.3/labels/adjudicated.jsonl` as `{"id", "final_label", "note"}`. The items' `label` / `ground_truth_chunks` fields are rater A's until then.

## Source-level checks (not in the label queue)
These are opinion-level questions for you, flagged during generation. They don't change any label.
- [ ] **Hamilton v. Dallas County, 5th Cir. 2022 panel opinion** (`cl7797513`; used by `title_vii_retaliation-qa-5`, `-cc-2`, `-cc-3`): later reheard en banc and abrogated (79 F.4th 494, 5th Cir. 2023). It is a published majority opinion, so §2 does not bar it. Its law is superseded, though, which is a poor look in a registry dataset. Keep, or swap for the en banc opinion and redraft 3 items?
- [ ] **Estate of Najera Aguirre** (`cl10820676`, 9th Cir.): the caption lists three plaintiffs by initials (likely minors). No item uses the caption or summary chunks. Keep under §2 ("name or describe a minor")?
- [ ] **Per curiam opinions kept as full merits opinions, not summary orders:** Norman v. Ingle (5th Cir.), Marcus & Millichap v. Triex and Lennar Homes v. Rafiei (Tex.).

## Disagreements and bad-item flags (17)

### [ ] agency_arbitrary_capricious-qa-2 · qa_citation · Shenzhen Youme v. FDA (ca5, 2025-08-06)

Source: [https://www.courtlistener.com/opinion/10649060/shenzhen-youme-v-fda/](https://www.courtlistener.com/opinion/10649060/shenzhen-youme-v-fda/) · opinion 11115647 · cited authority as it appears: `Calumet Shreveport Refin., L.L.C. v. EPA, 86 F.4th 1121, 1135 (5th Cir. 2023)`

**Question:** In Shenzhen Youme v. FDA, what must an agency do when it changes a policy, and when may a regulated party justifiably rely on a past practice?

**Reference notes:** Must mention: agencies may change policy if they display awareness of the change and give good reasons; an agency cannot surprise a party that relied in good faith on its prior position; reliance on a longstanding practice is justifiable until the agency publishes notice of a change; a legitimate reliance interest is a high bar.

**Chunks either rater chose:**

`cl11115647:11`

> The Supreme Court has since vacated our holding in Wages & White Lion. See Wages & White Lion, 145 S. Ct. 898. The Court left open whether arguments relying on an agency’s change in position applied to nonbinding agency guidance.4 We assume, without deciding, they do. “Agencies are free to change their existing policies as long as they provide a reasoned explanation for the change.” Encino Motorcars, LLC v. Navarro, 579 U.S. 211, 221 (2016). The first question is whether the “agency changed existing policy,” i.e., effected “a reversal of [its] former views as to the proper course” or “‘disavow[ed] prior ‘inconsistent’ agency action as ‘no longer good law.’” Wages & White Lion, 145 S. Ct. at 918 (first alteration in original) (first quoting State Farm, 463 U.S. at 41; and then quoting FCC v. Fox Television Stations, Inc., 556 U.S. 502, 517 (2009)). The second question is “[d]id the agency ‘display awareness that it is changing position’ and offer ‘good reasons for the new policy.’” Id. (quoting Fox Television Stations, 556 U.S. at 515).
>
> Youme argues that its testing of e-liquids “seemed to satisfy FDA’s recommendation in its PMTA Guidance” that they test with a “reasonable range of available e-liquids.” FDA concluded the “‘test data lack[ed] sufficient information to demonstrate potential nicotine exposure to users’ because ‘FDA requires data from e-liquids with the highest and lowest nicotine concentrations, both with the highest VG concentration.’”
>
> _____________________
>
> 4 The Supreme Court “assume[d], without deciding, that the change-in-position doctrine applies to an agency’s divergence from a position articulated in nonbinding guidance documents.” Wages & White Lion, 145 S. Ct. at 918 n.5.
>
> No. 24-60060

`cl11115647:13`

> Although the TCA does not require multiple deficiency letters, Youme argues FDA’s prior practice of issuing multiple rounds of deficiency letters could be sufficient to create justifiable reliance on FDA’s past practice of its iterative review process. “Agencies are free to change their existing policies as long as they provide a reasoned explanation for the change.” Encino Motorcars, 579 U.S. at 221. The agency must, at a minimum, “‘display awareness that it is changing position’ and ‘show that there are good reasons for the new policy.’” Id. (quoting Fox Television Stations, 556 U.S. at 515). An agency “cannot ‘surprise’ a party by penalizing it for ‘good-faith reliance’ on the agency’s prior positions.” R.J. Reynolds Vapor Co., 65 F.4th at 189 (quoting Christopher v. SmithKline Beecham Corp., 567 U.S. 142, 156–57 (2012)). Continued reliance on longstanding and well-established practices are justifiable until the agency first publishes notice of its intent to change its policy. See Calumet Shreveport Refin., L.L.C. v. EPA, 86 F.4th 1121, 1135 (5th Cir. 2023), vacated on other grounds, 145 S. Ct. 1735 (2025). A legitimate reliance interest is a high bar, “requiring, for example, ‘decades of industry reliance on [an agency’s] prior policy.’” Wages & White Lion, 145 S. Ct. at 927 (alteration in original) (quoting Encino Motorcars, 579 U.S. at 222).
>
> FDA received applications to market nearly 27 million deemed products, with more than 6.5 million before September 2020. Combatting the Youth Vaping Epidemic by Enhancing Enforcement Against Illegal E-Cigarettes: Hearing before the S. Comm. on the Judiciary, 118th Cong. 5 (2024) (statement of Brian A. King, Director, Ctr. for Tobacco Prods.) https://perma.cc/6LXP-3F2Y. In June 2021, FDA announced that it intended to issue only one deficiency letter and base its decision on the

Candidate window: `cl11115647:11`, `cl11115647:12`, `cl11115647:13`, `cl11115647:14`, `cl11115647:15`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl11115647:13']` | cl11115647:13 states the change-in-policy requirements and the limits of reliance interests. |
| Rater B | `['cl11115647:11', 'cl11115647:13']` | cl11115647:13 states awareness and good reasons, no surprise of good-faith reliance, reliance justifiable until notice, and the high bar; cl11115647:11 also states awareness and good reasons for changing position. |

**Recommended:** `['cl11115647:11', 'cl11115647:13']` — B: chunk 11 quotes the awareness-and-good-reasons test, a Must-mention point (§3.1 rule 2: same point in two chunks → mark both).

**Final label:** ______

---

### [ ] agency_arbitrary_capricious-qa-3 · qa_citation · BNSF Railway v. FRA (ca5, 2023-03-15)

Source: [https://www.courtlistener.com/opinion/9383962/bnsf-railway-v-fra/](https://www.courtlistener.com/opinion/9383962/bnsf-railway-v-fra/) · opinion 9379438 · cited authority as it appears: `Encino Motorcars, LLC v. Navarro, 579 U.S. 211, 221 (2016)`

**Question:** Why did the Fifth Circuit in BNSF Railway v. FRA vacate the agency's denial of the railroad's waiver request?

**Reference notes:** Must mention: agency action must be upheld, if at all, on the basis the agency itself articulated; the FRA articulated barely any basis, which was especially glaring given its safety mandate and BNSF's evidence that the technology was safer; so the agency had to provide further justification and the case was remanded.

**Chunks either rater chose:**

`cl9379438:5`

> that runs counter to the evidence before the agency, or is so
>
> implausible that it could not be ascribed to a difference in view
>
> or the product of agency expertise. Motor Vehicle Mfrs., 463 U.S. at 43.
>
> Finally, an “‘agency’s action must be upheld, if at all, on the basis articulated by the agency itself,’ not reasons developed post hoc.” 4 Although “we may not provide a reasoned basis for the agency’s action that the agency itself has not given,” we will “uphold a decision of less than ideal clarity if the agency’s path may reasonably be discerned.” Id. at 44 (internal quota-tions removed).
>
> III.
>
> BNSF presents a litany of reasons that the FRA’s decision was arbi-trary and capricious: BNSF claims that the FRA did not sufficiently consider safety in coming to its decision, 5 that its stated reason for denying BNSF’s exemption was without merit, and that its decision violates a condition FRA laid out for BNSF. 6 BNSF further claims that the FRA engendered reliance
>
> Texas, 40 F.4th at 226–27 (quoting Motor Vehicle Mfrs., 463 U.S. at 50); see also Dep’t of Homeland Sec. v. Regents of the Univ. of Cal., 140 S. Ct. 1891, 1907 (2020) (“It is a ‘foundational principle of administrative law’ that judicial review of agency action is lim-ited to ‘the grounds that the agency invoked when it took the action.’” (quoting Michigan v. EPA, 576 U.S. 743, 758 (2015))).
>
> See 49 U.S.C. § 103(c) (“In carrying out its duties, the [FRA] shall consider the assignment and maintenance of safety as the highest priority, recognizing the clear intent, encouragement, and dedication of Congress to the furtherance of the highest degree of safety in railroad transportation.”); id. § 20103(d)(1) (allowing the FRA to grant waivers “consistent with railroad safety”).
>
> The waiver granting BNSF’s second exemption request claimed to “provid[e] specific conditions, which if met, will allow BNSF to expand implementation of the relief in a consistent and safe manner.”
>
> No. 22-60217 interests by championing ATI and then changing its overall attitude toward ATI without formally announcing its now policy or reasoning through it. 7

`cl9379438:6`

> Perhaps these contentions have merit; maybe they do not. But unfor-tunately for the FRA, “[a]n agency’s action must be upheld, if at all, on the basis articulated by the agency itself,” Texas, 40 F.4th at 226–27, and here, the agency has barely articulated any basis at all. The paucity of reasoning is especially glaring in the face of the agency’s statutory mandate to prioritize safety. BNSF has made evidence-based claims that ATI is safer and more efficient than visual inspection alone. The implementation of ATI pursuant to the prior waiver appears to have been an unqualified success. The FRA is thus duty-bound to provide further justification for its rejection of the tech-nology’s expansion.
>
> We reiterate: “[A]gency action [must] be reasonable and reasonably explained.” Prometheus Radio Project, 141 S. Ct. at 1158. The agency must “articulate a satisfactory explanation for its action including a ‘rational con-nection between the facts found and the choice made.’” Motor Vehicle Mfrs., 463 U.S. at 43 (quoting Burlington Truck Lines, 371 U.S. at 168). Finding the FRA’s letter lacking in this regard, we GRANT review, VACATE, and REMAND for reconsideration. This is a limited remand; this panel retains jurisdiction. We direct the FRA to enter its decision no later than one hun-dred days from the announcement of this opinion.
>
> An agency must “provide a reasoned explanation for the change,” “at least ‘dis-play awareness that it is changing position[,]’ and ‘show that there are good reasons for the new policy.’” Encino Motorcars, LLC v. Navarro, 579 U.S. 211, 221 (2016) (quoting FCC v. Fox Television Stations, Inc., 556 U.S. 502, 515 (2009)). When reliance interests have been engendered by an existing policy, “an ‘[u]nexplained inconsistency’ in agency policy is ‘a reason for holding [a decision] to be an arbitrary and capricious change from agency practice.’” Id. (quoting Nat’l Cable & Telecomms. Ass’n v. Brand X Internet Servs., 545 U.S. 967, 981 (2005)).

Candidate window: `cl9379438:2`, `cl9379438:3`, `cl9379438:4`, `cl9379438:5`, `cl9379438:6`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl9379438:6']` | cl9379438:6 explains the paucity of reasoning, the safety mandate, and the vacatur and remand. |
| Rater B | `['cl9379438:5', 'cl9379438:6']` | cl9379438:6 says action must be upheld on the agency's articulated basis, the agency barely articulated any basis despite safety mandate and BNSF's evidence, so vacate and remand; cl9379438:5 also states the articulated-basis rule. |

**Recommended:** `['cl9379438:5', 'cl9379438:6']` — B: chunk 5 states the 'upheld, if at all, on the basis articulated by the agency' rule, the first Must-mention point.

**Final label:** ______

---

### [ ] arbitration_enforce-qa-1 · qa_citation · William Pace v. Hamilton Cove (nj, 2024-07-10)

Source: [https://www.courtlistener.com/opinion/9999010/william-pace-v-hamilton-cove/](https://www.courtlistener.com/opinion/9999010/william-pace-v-hamilton-cove/) · opinion 10465611 · cited authority as it appears: `Davis v. Oasis Legal Fin. Operating Co., 936 F.3d 1174, 1183`

**Question:** In Pace v. Hamilton Cove, why did the New Jersey Supreme Court say the Appellate Division's reliance on FLSA-based decisions did not support a rule that class action waivers are unenforceable outside arbitration?

**Reference notes:** Must mention: those decisions rested on statutes in which the legislature expressly conferred a right to proceed as a class; such legislation supports the premise that waivers can otherwise be enforceable rather than that they are always unenforceable outside arbitration; the Eleventh Circuit decision in Davis likewise turned on Georgia statutes.

**Chunks either rater chose:**

`cl10465611:18`

> Legislatures can override the freedom to contract in specific settings. Indeed, to support the proposition that “[c]lass action waivers have been declared unenforceable outside of the arbitration context in some jurisdictions,” the Appellate Division cites two cases applying the Fair Labor Standards Act of 1938 (FLSA), 29 U.S.C. §§ 201 to 219, in which Congress specifically provided that the statute could be enforced through a class action. 2 See Hamilton Cove, 475 N.J. Super. at 578 n.1; 29 U.S.C. § 216(b) (“An action to recover the liability prescribed in the preceding sentences may be maintained against any employer . . . by any one or more employees for and in behalf of himself or themselves and other employees similarly situated.”); see also Killion v. KeHE Distribs., LLC, 761 F.3d 574, 592 (6th Cir. 2014) (“Because no arbitration agreement is present in the case before us, we find no countervailing federal policy that outweighs the policy articulated in the The Appellate Division also included a cf. citation to a New Mexico case, Fiser v. Dell Computer Corp., 188 P.3d 1215 (N.M. 2008), to support its contention that class action waivers without an arbitration provision have been found unenforceable in other jurisdictions. Hamilton Cove, 475 N.J. Super. at 578 n.1. As explained in Fiser, however, New Mexico had also enacted specific statutory provisions that prohibited class action waivers in the arbitration context. 188 P.3d at 1219. The Supreme Court of New Mexico in that case noted that “the New Mexico Uniform Arbitration Act declares that arbitration clauses that require consumers to decline participation in class actions are unenforceable and voidable,” citing N.M. Stat. Ann. §§ 44-7A-1(b)(4)(f) and 44-7A-5. Ibid. The court further acknowledged that although those provisions might “be preempted by the FAA, it is clear evidence of the fundamental New Mexico policy of allowing consumers a means to redress their injuries via the class action device.” Ibid. (citation omitted). We have no such statutory provisions in New Jersey. FLSA.” (emphasis added)); Hall v. U.S. Cargo & Courier Serv., LLC, 299 F. Supp. 3d 888, 893 (S.D. Ohio 2018) (applying Killion and explaining that, in Killion, “[t]he Sixth Circuit held that employees cannot waive their rights under the FLSA, including their right to join collective actions, where no arbitration agreement exists” (emphasis added)).

`cl10465611:19`

> The Appellate Division did not discuss the role the text of the FLSA played in the decisions it cites. See Hamilton Cove, 475 N.J. Super. at 578 n.1. But the fact that certain legislation may expressly confer a right to file a class action, thereby forestalling attempts to contract around class actions, strongly supports the premise that class action waivers can be enforceable and not the proposition that they are always unenforceable outside the arbitration context.
>
> The Eleventh Circuit, for example, recently affirmed a district court decision that struck down a class action waiver outside the arbitration context because the waiver contravened “the Georgia Legislature’s intent to preserve class actions as a remedy for those aggrieved by payday lenders.” Davis v. Oasis Legal Fin. Operating Co., 936 F.3d 1174, 1183 (11th Cir. 2019). The statutes at issue in Davis expressly permitted plaintiffs to proceed through class actions in certain circumstances. See id. at 1181 (quoting the statutes); see also Ga. Code Ann. § 16-17-3 (“A civil action under [Georgia’s Payday Lending Act] may be brought on behalf of an individual borrower or on behalf of an ascertainable class of borrowers. In a successful action to enforce the provisions of this chapter, a court shall award a borrower, or class of borrowers, costs including reasonable attorneys’ fees.”); Ga. Code Ann. § 7-3-50(g) (“A claim of violation of [Georgia’s Installment Loan Act] against a licensee may be asserted in an individual action only and may not be the subject of a class action under [Ga. Code Ann. §] 9-11-23 or any other provision of law. A claim of violation of this chapter against an unlicensed lender may be asserted in a class action under [Ga. Code Ann. §] 9-11-23 or any other provision of law.”).

Candidate window: `cl10465611:17`, `cl10465611:18`, `cl10465611:19`, `cl10465611:20`, `cl10465611:21`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl10465611:19']` | cl10465611:19 explains the FLSA-based authorities turned on express statutory class-action rights, says that supports enforceability of waivers otherwise, and describes Davis as resting on Georgia statutes. |
| Rater B | `['cl10465611:18', 'cl10465611:19']` | Chunk 18 says the FLSA cases rested on Congress expressly providing for class actions; chunk 19 says such legislation supports enforceable waivers, not that they are always unenforceable, and that Davis rested on Georgia statutes. |

**Recommended:** `['cl10465611:18', 'cl10465611:19']` — B: chunk 18 states the FLSA cases rest on Congress expressly providing for class actions (point 1).

**Final label:** ______

---

### [ ] arbitration_enforce-qa-5 · qa_citation · Lennar Homes of Texas Inc. Lennar Homes of Texas Land and Construction, Ltd. Lennar Homes of Texas Sales and Marketing, Ltd. v. Mohammad Rafiei (tex, 2024-04-05)

Source: [https://www.courtlistener.com/opinion/9491475/lennar-homes-of-texas-inc-lennar-homes-of-texas-land-and-construction/](https://www.courtlistener.com/opinion/9491475/lennar-homes-of-texas-inc-lennar-homes-of-texas-land-and-construction/) · opinion 9958088 · cited authority as it appears: `In re U.S. Home Corp., 236 S.W.3d 761, 764`

**Question:** According to the Texas Supreme Court in Lennar Homes v. Rafiei, why was the homeowner's evidence of AAA fee schedules not enough to show the delegation clause was unconscionable?

**Reference notes:** Must mention: he offered no evidence of how the fee schedule would apply to resolving the arbitrability issue; he did not show he sought a fee deferral or reduction or a single arbitrator; a proper analysis compares litigation and arbitration costs and the claimant's ability to pay the difference.

**Chunks either rater chose:**

`cl9958088:5`

> The AAA Administrative Fee Schedules provide that a claimant instituting an action with damages of over $1 million must pay a filing fee of either $7,000 under the Standard Fee Schedule or $3,500 under the Flexible Fee Schedule. Under the Standard Fee Schedule, the parties owe an additional $7,700 if the case proceeds to a hearing. Under the Flexible Fee Schedule, the parties owe an additional $5,700 as a “Proceed Fee” and $7,700 if the case continues to a hearing. 2 These schedules provide some evidence regarding the fee for arbitrating the threshold issue of unconscionability.
>
> In addition to owing his share of these fees, Rafiei would owe half the cost of the arbitrators’ hourly rates and associated expenses under the parties’ agreement. 3 Although price lists are evidence of what Rafiei could be expected to pay, our Court has held that this falls short of “specific evidence that th[is] particular part[y] will be charged excessive fees.” Shattenkirk, 669 S.W.3d at 396 (quoting Olshan, 328 S.W.3d at 897). Rather, a party must adduce some evidence of a fee schedule as it is applied to resolve an arbitrability issue in his particular case.
>
> In In re Olshan, a foundation repair company and the homeowners who sued it had agreed to arbitrate their claims. 328 S.W.3d at 886-87. In concluding that the evidence was insufficient to establish unconscionability, we noted that “there is no evidence that the homeowners have made any effort to reduce the likely charges through requests for fee waivers, pro bono arbitrators, or even simply requesting a one arbitrator panel.” Id. at 897; see also In re FirstMerit Bank, N.A., 52 S.W.3d 749, 757 (Tex. 2001) (holding that the plaintiffs failed to
>
> 2 For non-monetary claims, the initial filing fee is $3,250 or $2,000, depending on the fee schedule. The fee schedules provide that “[t]he non-monetary filing fee is the minimum filing fee for any case requesting non-monetary relief. Where a party seeks both monetary damages and non-monetary relief, the higher of the two filing fees will apply.”

`cl9958088:6`

> 3 The arbitration agreement provides that “each party shall bear its own costs and expenses, including attorneys’ fees and paraprofessional fees, for any mediation and arbitration.” present legally sufficient evidence of unconscionability and noting that the AAA may defer or reduce fees in cases of extreme hardship).
>
> Similar to the plaintiffs in Olshan and FirstMerit Bank, in this case, Rafiei did not adduce evidence of how the fee schedule would be applied to resolve the unconscionability issue. Construction Industry Arbitration Rule 56 provides that “[t]he AAA may, in the event of extreme hardship on the part of any party, defer or reduce the administrative fees.” AAA, CONSTRUCTION INDUSTRY ARBITRATION RULES AND MEDIATION PROCEDURES Rule 56, at 35 (2024) (previously at Rule 55 (2015)). Like the homeowners in Olshan, Rafiei has presented no evidence that he sought a deferral or reduction of the administrative fees or an agreement to proceed with a single arbitrator. Without evidence that Rafiei sought to estimate the actual costs associated with arbitrating the arbitrability question, it is speculative to conclude that the delegation provision is itself unconscionable. “[M]aking the required showing entails presenting more than evidence of the ‘risk’ of incurring excessive costs; it requires ‘specific evidence that a party will actually be charged excessive arbitration fees.’” Shattenkirk, 669 S.W.3d at 395 (quoting In re U.S. Home Corp., 236 S.W.3d 761, 764 (Tex. 2007)). One may not “assume the most expensive possible scenario.” Olshan, 328 S.W.3d at 897 (citation omitted).
>
> A proper unconscionability analysis further requires a comparison of the relevant costs between litigating in court and in arbitration and of the claimant’s ability to pay the difference in such costs. “[W]e cannot assess whether [estimated arbitration] fees are what would prohibit [a claimant] from pursuing his rights without knowing (1) how that amount relates to the overall expense of litigating versus arbitrating and (2) [the claimant’s] ability to afford the former but not the latter.” Shattenkirk, 669 S.W.3d at 397; see also Olshan, 328 S.W.3d at 897.

`cl9958088:7`

> In Shattenkirk, a former employee opposed arbitration of a claim against his employer on the ground that excessive costs rendered any agreement to arbitrate unconscionable. 669 S.W.3d at 394. The employee averred that paying “anything above” the cost to litigate would cause him financial hardship. Id. at 397. Noting the evidence about costs and ability to pay was “quite vague and conclusory,” we held it insufficient to demonstrate unconscionability. Id.
>
> The evidence in this case is similarly vague. While the attorney’s supporting affidavit says that the cost of arbitration is “astronomically higher” than litigation, that the out-of-pocket expenses in litigation are “minimal,” and that hearings and trial are “free,” he does not quantify these differences with an estimate related to a hearing on the delegation clause in the arbitral forum. “[A]bsent concrete evidence that the increased cost associated with arbitration, compared to litigation, is what forecloses a party from pursuing his claims, the party cannot show that those costs are what make the expense of arbitrating ‘prohibitive.’” Id.; see also Olshan, 328 S.W.3d at 897 (“Even if we took these invoices as evidence of the likely arbitration charges to the [plaintiffs], they have provided no comparison of these charges to the expected cost of litigation . . . or their ability to pay these costs.”).
>
> More important, Rafiei’s affidavit fails to establish that he can afford litigation but not arbitration. Though he avers that he cannot afford more than $6,000 in “upfront costs,” he does not detail his available resources or lack of ability to pay. Rather, he notes that he has $6,000 in surplus income each month; he does not explain why this surplus is unavailable to pay for fees associated with arbitration of the unconscionability issue. 4 Unconscionability cannot be established absent evidence of “the claimant’s overall ability to pay the arbitration fees and costs.” Shattenkirk, 669 S.W.3d at 395 (quoting Olshan, 328 S.W.3d at 895). Even assuming that the evidence was sufficient to conclude that it would cost $8,025 to arbitrate the unconscionability issue, Rafiei’s affidavit fails to show that he cannot afford it.

Candidate window: `cl9958088:4`, `cl9958088:5`, `cl9958088:6`, `cl9958088:7`, `cl9958088:8`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl9958088:6']` | cl9958088:6 states Rafiei did not adduce evidence of how the fee schedule applies, did not seek a deferral or single arbitrator, and that analysis requires a cost comparison and ability to pay. |
| Rater B | `['cl9958088:5', 'cl9958088:6', 'cl9958088:7']` | Chunk 5 says a party must adduce evidence of fee schedule as applied; chunk 6 says no evidence of application, no deferral/reduction or single arbitrator sought, and requires cost comparison and ability to pay; chunk 7 requires ability-to-pay and litigation-vs-arbitration comparison evidence. |

**Recommended:** `['cl9958088:5', 'cl9958088:6', 'cl9958088:7']` — B: chunk 5 says a party must adduce evidence of the fee schedule as applied (point 1); chunk 7 requires the litigation-vs-arbitration cost and ability-to-pay comparison (point 3).

**Final label:** ______

---

### [ ] contract_interpretation-qa-3 · qa_citation · Chester Water Auth, Aplt. v. Pa. DCED (pa, 2021-04-29)

Source: [https://www.courtlistener.com/opinion/4878477/chester-water-auth-aplt-v-pa-dced/](https://www.courtlistener.com/opinion/4878477/chester-water-auth-aplt-v-pa-dced/) · opinion 4682256 · cited authority as it appears: `N. Hills News Record v. Town of McCandless, 555 Pa. 51, 58, 722 A.2d 1037, 1040 (1999)`

**Question:** Why did the Pennsylvania Supreme Court in Chester Water Authority v. Department of Community and Economic Development hold that the Right-to-Know Law's 'internal' deliberation exception does not reach communications with private consultants?

**Reference notes:** Must mention: consultants and their subcontractors are not agencies, members, employees or officials; 'internal' ordinarily means within the organization; clear text controls and exceptions are narrowly construed.

**Chunks either rater chose:**

`cl4682256:9`

> There is no dispute that the materials for which the Department has invoked the statutory privilege in issue are public records of an agency as defined in the RTKL and thus subject to public disclosure unless the exception applies. See generally 65 P.S. §67.701 (“Unless otherwise provided by law, a public record . . . shall be accessible for inspection and duplication in accordance with this act.”). Both parties also apprehend that, consistent with the Law's goal of promoting government transparency and its remedial nature, see SWB Yankees LLC v. Wintermantel, 615 Pa. 640, 662, 45 A.3d 1029, 1042 (2012) (explaining that the objective of the RTKL is to empower citizens by affording them access to information concerning the activities of their government), exceptions to the requirement for disclosure of public records are to be narrowly construed. See Grove, 640 Pa. at 25, 161 A.3d at 892.
>
> As the Authority stresses, Section 708(b)(10)(i)(A) prohibits disclosure of “internal, predecisional deliberations of an agency, its members, employees or officials,” as well a s deliberations between such individuals and another agency. 65 P.S. §67.708(b)(10)(i)(A) (emphasis added). As a third-party contractor and subcontractors, (…continued) consultants -- justifying application of what could be termed an “Act 47 consultant corollary.” See, e.g., id. at 18-19, 22. While the consultant corollary is supported by a colorable policy -based rationale, a broader “third -party contractor corollary” is both non -textual and lacks any similar ly focused justification. We also believe that, had the General Assembly intended uniquely for communications between agencies and Act 47 recovery coordinators -- but not other consultants -- to be excepted from the general requirement for disclosure under the RTKL, it would have said so. Accordingly, our remaining analysis is of the viability of a generalized consultant corollary under the Law.

`cl4682256:10`

> [J-75A&B-2020] - 10 Econsult and the Fairmount Capital and McNees firms plainly are not agencies,12 members, employees or officials.13 Accord Rojas, 927 F.3d at 1055 (“A third-party consultant . . . is not an agency” and “’neither the terms of the exemption nor the statutory definitions say anything about communications with outsiders.’” (quoting Klamath, 532 U.S. at 9, 121 S. Ct. at 1060)). See generally John C. Brinkerhoff Jr., FOIA's Common Law, 36 YALE J. ON REG. 575, 582–84 (2019) (criticizing that consultant corollary on the basis that “[i]t is doubtful that any reasonable reading of ‘inter-agency or intra-agency’ could encompass third parties”). And “internal,” relative to organized structures, commonly means “of, relating to, or occurring on the inside” -- or, in other words, within -- the organization. MERRIAM-WEBSTER DICTIONARY, https://www.merriam-webster.com/dictionary/internal (last visited Apr. 27, 2020).
>
> Accordingly, the statutory provision facially does not apply to communications with outside consultants. See generally N. Hills News Record v. Town of McCandless, 555 Pa. 51, 58, 722 A.2d 1037, 1040 (1999) (explaining that, where the provisions of a statute are clear, courts “ are forbidden from diverging from the plain meaning under the mere pretext of pursuing the spirit of the enactment. ”). And the requirement of narrow construction further solidifies the interpretation that private consultants providing services as independent contractors do not qualify as agencies, members, employees, or officials who may engage in protected internal communications. 12 The RTKL defines “agency” to mean four agencies (Commonwealth, Local, Legislative, and Judicial), all of which have specific definitions centered on governmental status. See 65 P.S. §67.102. None of the definitions include outsiders. 13 The words “members, employees or officials” are all undefined in the Law, and thus, we take them according to their common meaning. See Grove, 640 Pa. 1 at 25, 161 A.3d at 892 (citing 1 Pa.C.S. §1903(a)).
>
> [J-75A&B-2020] - 11

Candidate window: `cl4682256:8`, `cl4682256:9`, `cl4682256:10`, `cl4682256:11`, `cl4682256:12`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl4682256:10']` | cl4682256:10 reasons from the plain meaning of 'internal' and the status of outside consultants, plus narrow construction. |
| Rater B | `['cl4682256:9', 'cl4682256:10']` | cl4682256:10 says consultants are not agencies/members/employees/officials and 'internal' means within the organization; cl4682256:9 says exceptions to disclosure are narrowly construed. |

**Recommended:** `['cl4682256:9', 'cl4682256:10']` — B: chunk 9 states that exceptions to disclosure are narrowly construed (point 3).

**Final label:** ______

---

### [ ] first_amendment_employee-cc-5 · citation_check · Ciarametaro v. City of Gloucester (ca1, 2023-11-28)

Source: [https://www.courtlistener.com/opinion/9447400/ciarametaro-v-city-of-gloucester/](https://www.courtlistener.com/opinion/9447400/ciarametaro-v-city-of-gloucester/) · opinion 9905225 · cited authority as it appears: `Mihos v. Swift, 358 F.3d 91 (1st Cir. 2004)`

**Claim:** The First Circuit concluded that the city officials' worries about disruption were reasonable, noting that the fishermen's association had told the mayor it viewed the Harbormaster's Office as anti-fisherman.

**Cited passage:** `cl9905225:8`

> Ciarametaro's brief concedes that the City Officials were, in fact, "concerned" that his speech was causing local fishermen to "question the continued successes of the fleet in Gloucester." City Officials expressed such concerns immediately upon learning about Ciarametaro's involvement in the Lane case in April 2020. In his phone call with Ciarametaro, Destino emphasized the public perception risks of the City Harbormaster testifying against a local fisherman. Theken wrote in a text message to Ciarametaro that the testimony created a "big conflict" that could drive the fishing community to "lose trust" in the Harbormaster's Office. And Payson stated in an email that Ciarametaro's Lane testimony sent a "clear message" to the fishing community that the Harbormaster may not support them in a similar tort suit.
>
> The City Officials' concerns about the disruptive impact of Ciarametaro's testimony were certainly reasonable. Indeed, the organization representing many local fishermen -- the MLA -- expressly told Theken that those fishermen considered the Harbormaster's Office to be "anti-fisherman." Given that blunt language, the City Officials could reasonably predict that Ciarametaro's testimony risked undermining his ability to "[p]romote the City as a hospitable port of call." Ciarametaro himself was aware of this risk. In his text messages with Theken, Ciarametaro acknowledged that his testimony threatened the "public perception" of his department.4
>
> This is therefore not a case like Mihos v. Swift, 358 F.3d 91 (1st Cir. 2004), in which the plaintiff alleged that the content of his speech -- rather than concerns about the impact of that speech on his job performance -- provoked his employer's retaliatory pique. Id. at 103–08. Here, Ciarametaro acknowledges that the City Officials were concerned about his testimony
>
> 4 At oral argument, Ciarametaro's counsel conceded that these text messages reflected Ciarametaro's belief that his testimony could disrupt the relationship between the Harbormaster's Office and the fishing community. alienating an important local industry. In sum, the defendants' side of the Pickering scale bears substantial weight.
>
> B.

<details><summary>Other passages available</summary>

`cl11110987:18`

> The district court found those allegations insufficient to state a claim for First Amendment retaliation. It emphasized that the attempted conversation occurred during working hours and was between Long and her “supervising judge.” Long, 2024 WL 4710695, at *5. Contrary to the district court’s conclusion, those allegations are sufficient to survive defendants’ motion to dismiss.
>
> First, that Long’s conduct involved, in significant part, a decision not to speak does not strip her of First Amendment protection. The First Amendment’s guarantee of freedom of speech “necessarily compris[es] the decision of both what to say and what not to say.” Riley v. Nat’l Fed’n of the Blind of North Carolina, Inc., 487 U.S. 781, 796–97 (1988) (emphasis in original). “The right to speak and the right to refrain from speaking are complementary components of the broader concept of individual freedom of mind.” Wooley v. Maynard, 430 U.S. 705, 714 (1977) (internal quotation marks omitted); see also Jackler, 658 F.3d at 241 (concluding that “it is clear that the First Amendment protects the rights of a citizen to refuse to retract a report to the police that he believes is true, to refuse to make a statement that he believes is false, and to refuse to engage in unlawful conduct”). Long’s refusal is, therefore, the sort of conduct that the First Amendment protects.
>
> Second, the district court gave too much weight to the location of Long’s speech and the person to whom she spoke. “Speech to a supervisor even in the workplace can be protected as that of a private citizen if it is not made pursuant to the employee’s official duties as an employee.” Ross, 693 F.3d at 307. The critical inquiry is whether Long, in refusing to converse with Byrne about the Commission’s investigation, was acting pursuant to her job duties; the location of the speech and the person to whom it was directed, while relevant, are not dispositive considerations.

`cl9905225:7`

> We start by analyzing the City Officials' Pickering interest in the efficient provision of public services. At the outset, Ciarametaro asserts that there is "no evidence that [his
>
> 3 Our analysis of Ciarametaro's federal claim under section 1983 applies equally to his state claim under the Massachusetts Civil Rights Act. The Massachusetts Supreme Judicial Court has made clear that the "[f]ederal system of immunity for discretionary functions under [section] 1983" also applies to claims brought under the Massachusetts Civil Rights Act. Duarte v. Healy, 537 N.E.2d 1230, 1232 (Mass. 1989). testimony] was disruptive to the [Harbormaster's Office] or the [City]." But an employer need not "allow events to unfold to the extent that the . . . destruction of working relationships is manifest before taking action." Curran, 509 F.3d at 49 (quoting Connick v. Myers, 461 U.S. 138, 152 (1983)). Instead, to assess the employer interests implicated by Ciarametaro's speech, the relevant question is whether the City Officials were reasonably concerned that Ciarametaro's expert testimony would disrupt relationships between commercial fishermen and the Harbormaster's Office. Id. (quoting Waters v. Churchill, 511 U.S. 661, 673 (1994)) ("[R]easonable [employer] predictions of disruption" receive significant weight under Pickering); see also Kinney v. Weaver, 367 F.3d 337, 364 (5th Cir. 2004) (en banc) ("The key limitation on preemptive action . . .is that [an employer's] predictions of disruption must be reasonable.").

`cl9905225:9`

> Were we required to decide finally whether the City Officials violated Ciarametaro's First Amendment rights, we would now need to balance the City's foregoing interests against the interests of Ciarametaro and the public in his Lane testimony. Garcetti, 547 U.S. at 420. This would be a delicate and "fact-intensive" inquiry. Fabiano v. Hopkins, 352 F.3d 447, 457 (1st Cir. 2003).
>
> But we need not undertake this inquiry. This is because the outcome of such a difficult and fact-bound analysis "can rarely be considered 'clearly established,' at least in the absence of closely corresponding factual or legal precedent." Frazier v. Bailey, 957 F.2d 920, 931 (1st Cir. 1992). And Ciarametaro identifies no "closely corresponding" precedent clearly establishing that the City Officials -- at the time of their actions -- could not restrict his expert testimony to preserve relationships with the Gloucester fishing community.
>
> In his brief, Ciarametaro indirectly cites to Rankin v. McPherson, 483 U.S. 378 (1987), where the Supreme Court noted that it is "clearly established that a State may not discharge an employee on a basis that infringes that employee's constitutionally protected interest in freedom of speech." Id. at 383. This simply begs the question. Ciarametaro's citation to Rankin tautologically presumes that his speech was protected. But whether and how clearly Ciarametaro's speech was protected in the first place is the crux of this entire dispute.

`cl11107767:24`

> First, there is no genuine dispute that Appellees met the fourth and fifth steps regarding England asking Burch to resign and subsequently attempting to remove Burch through the City Council. England testified at his deposition that he was motivated by the Options in Process document, which he interpreted as “a department head who was telling the mayor he would do what he wanted or he would be rid of him,” and which England believed “was cause for removal.” Gummersall confirmed this, and Burch acknowledged at his deposition that he believed England was motivated to ask for his resignation by both his yard sign and his city administrator proposal, which included the Options in Process document. As explained above, this is unprotected speech. There is no genuine dispute that England was justified in removing Burch based on it. See Eng, 552 F.3d at 1071 (“[A] government entity has broader discretion to restrict speech when it acts in its role as employer, but the restrictions it imposes must be directed at speech that has some potential to affect the entity’s operations.” (quoting Garcetti, 547 U.S. at 418)); Lane v. Franks, 573 U.S. 228, 242 (2014) (“[G]overnment employers often have legitimate ‘interest[s] in the effective and efficient fulfillment of [their] responsibilities to the public,’ including ‘promot[ing] efficiency and integrity in the discharge of official duties,’ and ‘maintain[ing] proper discipline in public service.’” (second through fourth alterations in original) (quoting Connick v. Myers, 461 U.S. 138, 150–51 (1983))).

</details>

| | Label | Reason |
|---|---|---|
| Rater A | `supported` | Step 1: cl9905225:8 says the officials' concerns 'were certainly reasonable' and that the MLA 'expressly told Theken that those fishermen considered the Harbormaster's Office to be "anti-fisherman"'. |
| Rater B | `unsupported_claim` | cl9905225:8 says the MLA told Theken (no stated role as mayor) the Harbormaster's Office was anti-fisherman; no passage says the mayor was told. |

**Recommended:** `unsupported_claim` — B under §3.2 as written: the passage says the MLA told 'Theken'; only cl9905225:2 (not in the context set) identifies Theken as mayor. Preferred alternative: reword the claim to say 'told Theken' and keep `supported`, which is what A built.

**Final label:** ______

---

### [ ] ineffective_assistance-qa-3 · qa_citation · Jeffrey Workman v. Superintendent Albion SCI (ca3, 2019-02-12)

Source: [https://www.courtlistener.com/opinion/4589785/jeffrey-workman-v-superintendent-albion-sci/](https://www.courtlistener.com/opinion/4589785/jeffrey-workman-v-superintendent-albion-sci/) · opinion 4367038 · cited authority as it appears: `Miller-El v. Cockrell, 537 U.S. 322`

**Question:** What two showings does Martinez v. Ryan require, according to the Third Circuit in Workman v. Superintendent, to excuse a procedural default of an ineffective-assistance-of-trial-counsel claim?

**Reference notes:** Must mention: the underlying trial-counsel claim must be substantial, having some merit, meaning reasonable jurists could debate the resolution; and state post-conviction counsel must have been ineffective under Strickland; the some-merit standard differs from the merits standard under Strickland.

**Chunks either rater chose:**

`cl4367038:8`

> A. Excusing Procedural Default Under Martinez
>
> v. Ryan
>
> Martinez recognizes a narrow exception to the doctrine of procedural default: “Inadequate assistance of counsel at initial-review collateral proceedings may establish cause for a prisoner’s procedural default of a claim of ineffective assistance at trial.”18 This exception is available to a petitioner who can show that: 1) his procedurally defaulted ineffective assistance of trial counsel claim has “some merit”19; and that 2) his state-post conviction counsel was “ineffective under the We have jurisdiction under 28 U.S.C. §§ 1291 and 2253. We review the legal conclusions of the District Court de novo. Johnson v. Rosemeyer, 117 F.3d 104, 109 (3d Cir. 1997). Martinez, 566 U.S. at 9. Id. at 14 (citing Miller-El v. Cockrell, 537 U.S. 322 (2003)). standards of Strickland v. Washington.”20 We explain these requirements in turn.
>
> The Underlying Claim Must Have
>
> “Some Merit”
>
> To excuse procedural default on an ineffective assistance of trial counsel claim under Martinez, that claim must be substantial—it must have “some merit.”21 Miller-El v. Cockrell, the case on which the Supreme Court based its description of what a “substantial claim” entails, concerns the standards for issuing a certificate of appealability. To demonstrate that his claim has some merit, a petitioner must “show that reasonable jurists could debate whether (or, for that matter, agree that) the petition should have been resolved in a different manner or that the issues presented were adequate to deserve encouragement to proceed further.”22

`cl4367038:9`

> This is different from the standard applied on the merits under Strickland v. Washington.23 That standard requires a petitioner to show counsel was “deficient,” meaning “that counsel made errors so serious that counsel was not functioning as the ‘counsel’ guaranteed to the defendant by the Sixth Amendment.”24 A petitioner must also show that “the deficient performance prejudiced the defense,” which “requires showing that counsel’s errors were so serious as to Id. Id. (citing Miller-El, 537 U.S. 322). Miller-El, 537 U.S. at 336 (internal citation, quotation marks, and alteration omitted). 466 U.S. 668 (1984). Id. at 687. deprive the defendant of a fair trial.”25 This is an exacting standard,26 reflecting the reluctance of the courts to second-guess strategic decisions made by counsel.
>
> State Post-Conviction Counsel Must Be
>
> Ineffective
>
> A substantial claim alone is not sufficient to excuse a petitioner’s procedural default. Martinez holds that state post-conviction counsel must be “ineffective under the standards of Strickland v. Washington” to excuse the procedural default of the underlying claim.27
>
> We have described Strickland as containing two prongs, both of which must be met to sustain a claim of ineffective assistance of counsel: the “performance” and “prejudice” prongs.28 The “performance” prong refers to Strickland’s Id.

`cl4367038:10`

> See Kimmelman v. Morrison, 477 U.S. 365, 382 (1986) (noting that the Strickland standard is “highly demanding”). Martinez, 566 U.S. at 14. See Bey v. Superintendent Greene SCI, 856 F.3d 230, 238 (3d Cir. 2017) (“To prove ineffective assistance of counsel under Strickland v. Washington, a petitioner must prove ‘(1) that his counsel’s performance was deficient, that is, it fell below an objective standard of reasonableness, and (2) that counsel’s deficient performance prejudiced his client,’ i.e., that ‘there is a reasonable probability that, but for counsel’s unprofessional errors, the result of the proceeding would have been different.’ We have previously referred to these as the ‘performance’ and ‘prejudice’ prongs of the Strickland test.” (citation omitted)). requirement that “counsel’s representation fell below an objective standard of reasonableness.”29 The “prejudice” prong refers to Strickland’s requirement that a petitioner show “a reasonable probability that, but for counsel’s unprofessional errors, the result of the proceeding would have been different.”30
>
> For Workman to show that his state post-conviction counsel’s deficient performance caused prejudice under Strickland, he must show that his state post-conviction counsel could have obtained a different result had he presented the now-defaulted ineffective-assistance-of-trial-counsel claim. In other words, he must prove the merits of his underlying ineffective-assistance-of-trial-counsel claim in order to excuse the procedural default of that claim and obtain consideration on the merits. At this stage, what is important is that the underlying ineffective-assistance-of-trial-counsel claim is “substantial,” not that a petitioner has, in fact, been “prejudiced” by trial counsel’s deficient performance under Strickland.
>
> If the use of the word “substantial” and the phrase “some merit” rather than “prejudicial” does not make it explicit, the Supreme Court clearly implies, by relying on Miller-El v. Cockrell in its requirement that the claim be substantial, that the underlying ineffective-assistance-of-trial-counsel claim must be evaluated under a standard less exacting than Strickland prejudice.31 In Martinez, the Court Strickland, 466 U.S. at 687–88. Id. at 694.
>
> See Martinez, 566 U.S. at 14; Bey, 856 F.3d at 238 (interpreting Martinez as “suggesting that we apply the acknowledged that an unrepresented or ineffectively represented prisoner likely cannot vindicate an ineffective-assistance-of-trial-counsel claim:

Candidate window: `cl4367038:6`, `cl4367038:7`, `cl4367038:8`, `cl4367038:9`, `cl4367038:10`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl4367038:8']` | cl4367038:8 states the two Martinez requirements and the some-merit standard borrowed from certificate-of-appealability law. |
| Rater B | `['cl4367038:8', 'cl4367038:9', 'cl4367038:10']` | Chunk 8 states the two Martinez showings and the some-merit/reasonable jurists test; chunk 9 states it differs from Strickland merits standard and post-conviction counsel must be ineffective; chunk 10 restates less-exacting standard. |

**Recommended:** `['cl4367038:8', 'cl4367038:9']` — Partly B: chunk 9 states the some-merit standard differs from Strickland merits and that PCR counsel must be ineffective (points 2–3); chunk 10 states no Must-mention point of this question.

**Final label:** ______

---

### [ ] ineffective_assistance-qa-4 · qa_citation · Jeffrey Workman v. Superintendent Albion SCI (ca3, 2019-02-12)

Source: [https://www.courtlistener.com/opinion/4589785/jeffrey-workman-v-superintendent-albion-sci/](https://www.courtlistener.com/opinion/4589785/jeffrey-workman-v-superintendent-albion-sci/) · opinion 4367038 · cited authority as it appears: `Brown v. Brown, 847 F.3d 502, 513`

**Question:** In Workman, how did the Third Circuit say the prejudice requirement for post-conviction counsel's ineffectiveness under Martinez is satisfied?

**Reference notes:** Must mention: the underlying claim is evaluated under a standard less exacting than Strickland prejudice; Martinez recognizes a prisoner likely needs an effective attorney to raise trial-counsel claims; the court agrees with the Seventh and Ninth Circuits that prejudice may be satisfied with a substantial underlying ineffective-assistance claim.

**Chunks either rater chose:**

`cl4367038:10`

> See Kimmelman v. Morrison, 477 U.S. 365, 382 (1986) (noting that the Strickland standard is “highly demanding”). Martinez, 566 U.S. at 14. See Bey v. Superintendent Greene SCI, 856 F.3d 230, 238 (3d Cir. 2017) (“To prove ineffective assistance of counsel under Strickland v. Washington, a petitioner must prove ‘(1) that his counsel’s performance was deficient, that is, it fell below an objective standard of reasonableness, and (2) that counsel’s deficient performance prejudiced his client,’ i.e., that ‘there is a reasonable probability that, but for counsel’s unprofessional errors, the result of the proceeding would have been different.’ We have previously referred to these as the ‘performance’ and ‘prejudice’ prongs of the Strickland test.” (citation omitted)). requirement that “counsel’s representation fell below an objective standard of reasonableness.”29 The “prejudice” prong refers to Strickland’s requirement that a petitioner show “a reasonable probability that, but for counsel’s unprofessional errors, the result of the proceeding would have been different.”30
>
> For Workman to show that his state post-conviction counsel’s deficient performance caused prejudice under Strickland, he must show that his state post-conviction counsel could have obtained a different result had he presented the now-defaulted ineffective-assistance-of-trial-counsel claim. In other words, he must prove the merits of his underlying ineffective-assistance-of-trial-counsel claim in order to excuse the procedural default of that claim and obtain consideration on the merits. At this stage, what is important is that the underlying ineffective-assistance-of-trial-counsel claim is “substantial,” not that a petitioner has, in fact, been “prejudiced” by trial counsel’s deficient performance under Strickland.
>
> If the use of the word “substantial” and the phrase “some merit” rather than “prejudicial” does not make it explicit, the Supreme Court clearly implies, by relying on Miller-El v. Cockrell in its requirement that the claim be substantial, that the underlying ineffective-assistance-of-trial-counsel claim must be evaluated under a standard less exacting than Strickland prejudice.31 In Martinez, the Court Strickland, 466 U.S. at 687–88. Id. at 694.
>
> See Martinez, 566 U.S. at 14; Bey, 856 F.3d at 238 (interpreting Martinez as “suggesting that we apply the acknowledged that an unrepresented or ineffectively represented prisoner likely cannot vindicate an ineffective-assistance-of-trial-counsel claim:

`cl4367038:11`

> Without the help of an adequate
>
> attorney, a prisoner will have
>
> similar difficulties vindicating a
>
> substantial ineffective-assistance-
>
> of-trial-counsel claim. Claims of
>
> ineffective assistance at trial often
>
> require investigative work and an
>
> understanding of trial strategy.
>
> When the issue cannot be raised on
>
> direct review, moreover, a prisoner
>
> asserting an ineffective-assistance-
>
> of-trial-counsel claim in an initial-
>
> review collateral proceeding
>
> cannot rely on a court opinion or
>
> the prior work of an attorney
>
> addressing that claim. . . . To
>
> present a claim of ineffective
>
> assistance at trial in accordance
>
> with the State’s procedures, then, a
>
> prisoner likely needs an effective
>
> attorney.
>
> The same would be true if the State
>
> did not appoint an attorney to assist
>
> in the initial-review collateral
>
> proceeding. The prisoner, standard for issuing certificates of appealability in resolving the inquiry into what constitutes a ‘substantial’ claim”).
>
> unlearned in the law, may not
>
> comply with the State’s procedural
>
> rules or may misapprehend the
>
> substantive details of federal
>
> constitutional law. . . . While
>
> confined to prison, the prisoner is
>
> in no position to develop the
>
> evidentiary basis for a claim of
>
> ineffective assistance, which often
>
> turns on evidence outside the trial
>
> record.32
>
> Martinez also recognizes that “[a] finding of cause and prejudice does not entitle the prisoner to habeas relief. It merely allows a federal court to consider the merits of a claim that otherwise would have been procedurally defaulted.”33
>
> Two other appellate courts have considered the role of Martinez’s “substantial” requirement and whether the underlying ineffective-assistance-of-trial-counsel claim must also be analyzed under the exacting bar of Strickland. In our view, and in accordance with the view shared by the Seventh and Ninth Circuits, when a petitioner shows that post-conviction relief counsel’s performance was unreasonably deficient, the requirement that the deficient performance result in prejudice may be satisfied “with a substantial claim of ineffective assistance of trial counsel that would otherwise have been deemed defaulted.”34 Martinez, 566 U.S. at 11–12 (internal citations omitted). Id. at 17. Brown v. Brown, 847 F.3d 502, 513 (7th Cir. 2017) (citing Detrich v. Ryan, 740 F.3d 1237, 1245–46 (9th Cir. 2013)).

`cl4367038:13`

> The Ninth Circuit also considered Justice Breyer’s statement “respecting the denial of the petition for the writ of Detrich, 740 F.3d at 1246. Id. at 1245. Id. at 1245–46. certiorari” in Gallow v. Cooper,41 understanding him to distinguish between “cause” under the second prong of Martinez and “cause and prejudice” under Strickland: “That is, cause and prejudice under Strickland are determined separately from, and after, a determination of ‘cause’ under Martinez.”42 Justice Breyer, who wrote for the Court in Trevino, wrote in Gallow that “[t]he ineffective assistance of state habeas counsel might provide cause to excuse the default of the claim, thereby allowing the federal habeas court to consider the full contours of Gallow’s ineffective-assistance claim.”43 We agree with the Ninth Circuit’s analysis. Whether the ineffectiveness of post-conviction relief counsel provided cause to excuse procedural default is separate from the question of whether an ineffective-assistance-of-trial-counsel claim would prevail on the merits.
>
> In Brown v. Brown,44 the Seventh Circuit adopted the Ninth Circuit’s rule as follows: “To demonstrate cause under Martinez-Trevino, the petitioner must show deficient performance by counsel on collateral review as required under the first prong of the Strickland analysis. . . . Actual resulting prejudice can be established with a substantial claim of ineffective assistance of trial counsel that would otherwise have been deemed defaulted.”45
>
> This rule is sensible, workable, and a proper reading of Martinez. If Workman shows that his underlying ineffective-570 U.S. 933 (2013). Detrich, 740 F.3d at 1246. Gallow, 570 U.S. at 933. 847 F.3d 502 (7th Cir. 2017) Id. at 513 (internal citations omitted). assistance-of-trial-counsel claim has some merit and that his state post-conviction counsel’s performance fell below an objective standard of reasonableness, he has shown sufficient prejudice from counsel’s ineffective assistance that his procedural default must be excused under Martinez.46
>
> B. Workman’s Underlying Claim Has “Some
>
> Merit”

Candidate window: `cl4367038:9`, `cl4367038:10`, `cl4367038:11`, `cl4367038:12`, `cl4367038:13`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl4367038:11']` | cl4367038:11 describes the less exacting standard, quotes Martinez on the need for an effective attorney and adopts the Seventh and Ninth Circuit view. |
| Rater B | `['cl4367038:10', 'cl4367038:11', 'cl4367038:13']` | Chunk 10 says the underlying claim is evaluated under a standard less exacting than Strickland prejudice; chunk 11 quotes Martinez that a prisoner likely needs an effective attorney and states agreement with the Seventh and Ninth Circuits; chunk 13 agrees with the Ninth Circuit's analysis. |

**Recommended:** `['cl4367038:10', 'cl4367038:11', 'cl4367038:13']` — B: chunk 10 states the 'less exacting than Strickland prejudice' standard (point 1); chunk 13 states agreement with the Ninth Circuit and quotes the Seventh's rule (point 3).

**Final label:** ______

---

### [ ] ineffective_assistance-qa-5 · qa_citation · People v. Roland (ill, 2023-11-30)

Source: [https://www.courtlistener.com/opinion/9448023/people-v-roland/](https://www.courtlistener.com/opinion/9448023/people-v-roland/) · opinion 9905848 · cited authority as it appears: `People v. Harris, 206 Ill. 2d 1, 16`

**Question:** Why did the Illinois Supreme Court in People v. Roland hold that the postconviction petition failed to show prejudice from counsel's omission of mental-health records?

**Reference notes:** Must mention: the trial court already knew of Roland's mental-health issues and suicide attempts yet found his conduct that day, fleeing and taking evasive measures, inconsistent with suicide by police; corroborating records would not likely have changed that focus, so no reasonable likelihood of a different outcome; the court therefore did not reach deficient performance.

**Chunks either rater chose:**

`cl9905848:10`

> for counsel’s deficient performance, the result of the proceeding would have been different. Id. (citing Domagala, 2013 IL 113688, ¶ 36). A reasonable probability is a probability sufficient to undermine confidence in the outcome. People v. Pingelton, 2022 IL 127680, ¶ 53. ¶ 27 We need not address Roland’s contention that his trial counsel’s failure to present the documents appended to his postconviction petition was objectively unreasonable because we conclude that Roland has failed to establish prejudice. See People v. Johnson, 2021 IL 126291, ¶ 53 (if it is easier to dispose of an ineffective-assistance claim on the ground that it lacks a showing of sufficient prejudice, a court may proceed directly to Strickland’s prejudice prong). Roland urges that his trial came down to a credibility contest between his testimony that he pointed the gun into the air and Officer Rewers’s testimony that Roland pointed the gun directly at him. He argues, as the appellate court found, evidence of his mental health would have corroborated his testimony and explained why he shot the gun into the air. Had this evidence been presented, therefore, there is a reasonable probability that his trial would have resulted in a different outcome. ¶ 28 We agree with Roland that the documents appended to his petition would have corroborated his uncontested testimony at trial regarding his mental health issues. Nonetheless, it does not necessarily follow that these documents, if admitted into evidence, would have changed the outcome of his trial. See id. ¶ 54 (an error by counsel, even if professionally unreasonable, does not warrant setting aside the judgment of a criminal proceeding if the error had no effect on the judgment). Indeed, in assessing prejudice under Strickland, the question is not whether counsel’s performance had no effect on the outcome or whether it is possible a reasonable doubt might have been established if counsel acted differently but, instead, whether it is reasonably likely that the result of the proceedings would have been different. People v. Lewis, 2022 IL 126705, ¶ 46. We cannot say that in this case there would have been a different

`cl9905848:11`

> outcome. ¶ 29 In asking whether Roland’s trial likely would have had a different outcome if trial counsel had presented the documents appended to his postconviction petition, we take note of the trial court’s specific comments about Roland running away from the police officers. The court said: “If he wanted to commit suicide by police *** [if he] wants to guarantee all three of them shooting at him, he wouldn’t be fleeing and running and ducking behind the archway.” As Roland acknowledges, the trial court was fully aware of his mental health issues and suicide attempts, but it nevertheless found that his conduct on that day did not support the defense that he wanted to commit “suicide by police.” In finding Roland guilty, the trial court focused on his fleeing from the police and not the credibility regarding his suicide attempts. Accordingly, it is unlikely that corroborating evidence that Roland had struggled with suicide on other occasions would have changed the trial court’s focus from his conduct on that particular day, such that the court would have found him not guilty. ¶ 30 In other words, it is not reasonably likely that further evidence of Roland’s mental health history would have changed the trial court’s determination that Roland’s conduct during the shooting did not demonstrate that he wanted to commit “suicide by police.” Specifically, the court noted that he fled from the police and their gunfire, taking evasive measures to avoid being shot. Accordingly, we find that Roland’s postconviction petition failed to satisfy the prejudice prong of Strickland. See People v. Harris, 206 Ill. 2d 1, 16 (2002) (in order to establish prejudice, the defendant must show that there is a reasonable probability that, but for counsel’s unprofessional errors, the result of the proceeding would have been different). Because Roland has failed to establish the prejudice prong required by Strickland, we need not address whether Roland’s petition satisfied the performance prong of Strickland. See People v. Gayden, 2020 IL 123505, ¶ 27 (the failure to establish either prong of the Strickland test precludes a finding of ineffective assistance of counsel).

Candidate window: `cl9905848:8`, `cl9905848:9`, `cl9905848:10`, `cl9905848:11`, `cl9905848:12`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl9905848:11']` | cl9905848:11 states the trial court's awareness, its focus on fleeing, the unlikelihood of a different result and that performance need not be reached. |
| Rater B | `['cl9905848:10', 'cl9905848:11']` | Chunk 11 states trial court knew of mental health issues but found fleeing inconsistent with suicide by police so no likely different outcome; chunk 10 says court need not address deficient performance. |

**Recommended:** `['cl9905848:10', 'cl9905848:11']` — B: chunk 10 (¶27) says the court need not address deficient performance (point 3).

**Final label:** ______

---

### [ ] limitations_discovery_rule-qa-4 · qa_citation · Marcus & Millichap Real Estate Investment Services of Nevada, Inc. v. Triex Texas Holdings, LLC, and Bryan Weiner (tex, 2023-01-13)

Source: [https://www.courtlistener.com/opinion/9367923/marcus-millichap-real-estate-investment-services-of-nevada-inc-v-triex/](https://www.courtlistener.com/opinion/9367923/marcus-millichap-real-estate-investment-services-of-nevada-inc-v-triex/) · opinion 9363399 · cited authority as it appears: `Valdez v. Hollenbeck, 465 S.W.3d 217, 231`

**Question:** Why did the Texas Supreme Court in Marcus & Millichap v. Triex hold that the discovery rule applied to the breach of fiduciary duty claim, and until when does the rule defer accrual?

**Reference notes:** Must mention: in the fiduciary context the injury is presumed inherently undiscoverable because fiduciaries are presumed to have superior knowledge and the beneficiary may be unaware of the need to inquire; when the rule applies, accrual is deferred until the plaintiff knew or, with reasonable diligence, should have known of the facts giving rise to the claim or the wrongful act and resulting injury.

**Chunks either rater chose:**

`cl9363399:4`

> The discovery rule is a “narrow exception” to the legal injury rule that “defers accrual of a cause of action until the plaintiff knew or, exercising reasonable diligence, should have known of the facts giving rise to the cause of action.” Berry, 646 S.W.3d at 524 (quoting Comput. Assocs. Int’l, Inc. v. Altai, Inc., 918 S.W.2d 453, 455 (Tex. 1996)). It “applies when the injury is by its nature inherently undiscoverable.” Agar Corp., 580 S.W.3d at 139 (citing Childs v. Haussecker, 974 S.W.2d 31, 36-37 (Tex. 1998)). “An injury is inherently undiscoverable if it is by nature unlikely to be discovered within the prescribed limitations period despite due diligence.” Berry, 646 S.W.3d at 524 (quoting S.V., 933 S.W.2d at 25). “The determination of whether an injury is inherently undiscoverable is made on a categorical basis rather than on the facts of the individual case.” Archer v. Tregellas, 566 S.W.3d 281, 290 (Tex. 2018) (citing HECI Expl. Co. v. Neel, 982 S.W.2d 881, 886 (Tex. 1998)). The question is whether the injury is “the type of injury that could be discovered through the exercise of reasonable diligence.” BP Am. Prod. Co. v. Marshall, 342 S.W.3d 59, 66 (Tex. 2011) (citing Wagner & Brown, Ltd. v. Horwood, 58 S.W.3d 732, 734-35 (Tex. 2001)).

`cl9363399:5`

> We have held that “in the fiduciary context, . . . the nature of the injury is presumed to be inherently undiscoverable” because “[f]iduciaries are presumed to possess superior knowledge.” Comput. Assocs., 918 S.W.2d at 456. So “[a] person to whom a fiduciary duty is owed may be unable to inquire into the fiduciary’s actions or may be unaware of the need to do so.” Valdez v. Hollenbeck, 465 S.W.3d 217, 231 (Tex. 2015). Accordingly, “even if inquiry is made, ‘[f]acts which might ordinarily require investigation likely may not excite suspicion where a fiduciary relationship is involved.’” Id. (quoting Willis v. Maverick, 760 S.W.2d 642, 645 (Tex. 1988)). Here the discovery rule applies, but it does not save Triex’s claims. The rule applies because a fiduciary relationship existed, 2 and before Taylor Petroleum’s breach, Triex was unaware of the need to inquire into its fiduciary’s actions. See S.V., 933 S.W.2d at 8 (explaining that the rationale for finding a fiduciary’s misconduct to be inherently undiscoverable is that “a person to whom a fiduciary duty is owed is either unable to inquire into the fiduciary’s actions or unaware of the need to do so”).
>
> When the discovery rule applies, the statute of limitations does not begin to run “until the plaintiff knew or in the exercise of reasonable diligence should have known of the wrongful act and resulting injury.” Id. at 4. We have stated this rule in slightly different ways. But last Term, we explained that this means the discovery rule defers accrual “until the claimant knew or should have known of facts that in the exercise of reasonable diligence would have led to the discovery of the wrongful act.” Berry, 646 S.W.3d at 524 (quoting Little, 943 S.W.2d at 420). Or, in other words, accrual is deferred “until the plaintiff knew, or exercising reasonable diligence, should have known of the facts giving rise to the cause of action.” Id. (quoting Comput. Assocs., 918 S.W.2d at 455). Consistent throughout our cases is the requirement of reasonable

Candidate window: `cl9363399:3`, `cl9363399:4`, `cl9363399:5`, `cl9363399:6`, `cl9363399:7`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl9363399:5']` | cl9363399:5 gives the fiduciary presumption of inherent undiscoverability and the reasonable-diligence formulations of when accrual is deferred. |
| Rater B | `['cl9363399:4', 'cl9363399:5']` | Chunk 5 states fiduciary injury presumed inherently undiscoverable and beneficiary may be unaware of need to inquire, and deferral until plaintiff knew or should have known; chunk 4 also states the discovery rule defers accrual until plaintiff knew or should have known of facts. |

**Recommended:** `['cl9363399:4', 'cl9363399:5']` — B: chunk 4 states the rule defers accrual until the plaintiff knew or should have known (point 2).

**Final label:** ______

---

### [ ] limitations_discovery_rule-qa-5 · qa_citation · Marcus & Millichap Real Estate Investment Services of Nevada, Inc. v. Triex Texas Holdings, LLC, and Bryan Weiner (tex, 2023-01-13)

Source: [https://www.courtlistener.com/opinion/9367923/marcus-millichap-real-estate-investment-services-of-nevada-inc-v-triex/](https://www.courtlistener.com/opinion/9367923/marcus-millichap-real-estate-investment-services-of-nevada-inc-v-triex/) · opinion 9363399 · cited authority as it appears: `PPG Indus., Inc. v. JMB/Hous. Ctrs. Partners Ltd. P’ship, 146 S.W.3d 79, 93`

**Question:** What did the Texas Supreme Court say in Marcus & Millichap that the discovery rule does not require the claimant to know before limitations begins to run?

**Reference notes:** Must mention: consistent throughout the cases is the requirement of reasonable diligence; the rule does not linger until the claimant learns of actual causes and possible cures; it does not defer accrual until the plaintiff knows the specific nature of each wrongful act or the exact identity of the wrongdoer.

**Chunks either rater chose:**

`cl9363399:5`

> We have held that “in the fiduciary context, . . . the nature of the injury is presumed to be inherently undiscoverable” because “[f]iduciaries are presumed to possess superior knowledge.” Comput. Assocs., 918 S.W.2d at 456. So “[a] person to whom a fiduciary duty is owed may be unable to inquire into the fiduciary’s actions or may be unaware of the need to do so.” Valdez v. Hollenbeck, 465 S.W.3d 217, 231 (Tex. 2015). Accordingly, “even if inquiry is made, ‘[f]acts which might ordinarily require investigation likely may not excite suspicion where a fiduciary relationship is involved.’” Id. (quoting Willis v. Maverick, 760 S.W.2d 642, 645 (Tex. 1988)). Here the discovery rule applies, but it does not save Triex’s claims. The rule applies because a fiduciary relationship existed, 2 and before Taylor Petroleum’s breach, Triex was unaware of the need to inquire into its fiduciary’s actions. See S.V., 933 S.W.2d at 8 (explaining that the rationale for finding a fiduciary’s misconduct to be inherently undiscoverable is that “a person to whom a fiduciary duty is owed is either unable to inquire into the fiduciary’s actions or unaware of the need to do so”).
>
> When the discovery rule applies, the statute of limitations does not begin to run “until the plaintiff knew or in the exercise of reasonable diligence should have known of the wrongful act and resulting injury.” Id. at 4. We have stated this rule in slightly different ways. But last Term, we explained that this means the discovery rule defers accrual “until the claimant knew or should have known of facts that in the exercise of reasonable diligence would have led to the discovery of the wrongful act.” Berry, 646 S.W.3d at 524 (quoting Little, 943 S.W.2d at 420). Or, in other words, accrual is deferred “until the plaintiff knew, or exercising reasonable diligence, should have known of the facts giving rise to the cause of action.” Id. (quoting Comput. Assocs., 918 S.W.2d at 455). Consistent throughout our cases is the requirement of reasonable

`cl9363399:6`

> 2 Marcus & Millichap did not challenge the existence of a fiduciary relationship on appeal. It argues in this Court in a footnote that it was an intermediary, but it did not present this argument below and has therefore waived the issue. diligence. We have also explained that “the discovery rule does not linger until a claimant learns of actual causes and possible cures.” PPG Indus., Inc. v. JMB/Hous. Ctrs. Partners Ltd. P’ship, 146 S.W.3d 79, 93 (Tex. 2004); see also KPMG Peat Marwick v. Harrison Cnty. Hous. Fin. Corp., 988 S.W.2d 746, 749 (Tex. 1999). Nor does it defer accrual until the plaintiff knows “the specific nature of each wrongful act that may have caused the injury,” KPMG, 988 S.W.2d at 749, or “the exact identity of the wrongdoer.” Childs, 974 S.W.2d at 40; see also PPG Indus., 146 S.W.3d at 93.

Candidate window: `cl9363399:4`, `cl9363399:5`, `cl9363399:6`, `cl9363399:7`, `cl9363399:8`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl9363399:6']` | cl9363399:6 states the reasonable-diligence requirement and lists causes, cures, specific nature of each wrongful act and exact identity of the wrongdoer as things the rule does not wait for. |
| Rater B | `['cl9363399:5', 'cl9363399:6']` | Chunk 5 ends with 'Consistent throughout our cases is the requirement of reasonable' (completed in 6); chunk 6 states the 'does not linger' and 'specific nature/exact identity' points. |

**Recommended:** `['cl9363399:5', 'cl9363399:6']` — B: the 'requirement of reasonable diligence' sentence splits across the boundary (§3.1 rule 3 → mark both).

**Final label:** ______

---

### [ ] miranda_custody-qa-4 · qa_citation · United States v. Doe (ca1, 2022-01-20)

Source: [https://www.courtlistener.com/opinion/6238504/united-states-v-doe/](https://www.courtlistener.com/opinion/6238504/united-states-v-doe/) · opinion 6105386 · cited authority as it appears: `United States v. Piper, 298 F.3d 47, 58 (1st Cir. 2002)`

**Question:** In United States v. Doe, why did the First Circuit conclude that any Miranda error in admitting the former immigration official's testimony was harmless?

**Reference notes:** Must mention: the government had to prove Doe knew he was not assigned the social security number, the official's testimony added little to that proof, and other evidence of guilt was overwhelming, including the testimony of the real assignee's brother and supporting documents.

**Chunks either rater chose:**

`cl6105386:9`

> To convict Doe of the offenses that he was indicted on, the government had to prove beyond a reasonable doubt that Doe knew that he was not assigned SSN xxx-xx-9645. The government's case thus depended on its ability to show beyond a reasonable doubt that the biographical information regarding José Manuel Rodriguez that Doe purported was his own was, in fact, not and that he knew it was not each time that he used that number in the manner that supplies the predicate for each of the charges on which the convictions that he challenges are based. But, that being so, we see no reason to conclude that DeChoudens's testimony "add[ed] very much [in the way of proof] to the mix." See United States v. Piper, 298 F.3d 47, 58 (1st Cir. 2002).
>
> Wholly apart from that testimony, the evidence the government presented to show that Doe was not José Manuel Rodriguez and knew that he was not was overwhelming. See Clark v. Moran, 942 F.2d 24, 27 (1st Cir. 1991) ("[C]ourts have found [an] error to be harmless when the [remaining] evidence . . . provided 'overwhelming evidence' of the defendant's guilt." (citation omitted)). For example, the government presented testimony from Angel Rodriguez, the brother of José Manuel Rodriguez -- the purported true assignee of SSN xxx-xx-9645 -- that his brother's biographical information matched the information the SSA had on file for the social security number that Doe was using. Specifically, Angel testified that his brother was born in Puerto Rico in 1949 to their parents, José Manuel Rodriguez and Felicita Nieves, and that his brother had died in 2012. To substantiate that testimony, the government introduced into evidence his brother's application for a social security number in 1964, his original social security card, and his death certificate.

`cl6105386:10`

> To be sure, Doe's sole witness, his daughter, did testify that Doe's birthdate was November 15, 1949 -- a birthdate that matched the SSA's records relating to SSN xxx-xx-9645. But, on cross examination, she admitted that she had applied for a U.S. passport roughly two decades earlier and had stated in doing so at that time that her father's birthdate was May 20, 1950. Nor did she explain the discrepancy between her representations about her father's birthdate in her testimony and her contradictory representation about it when she had applied for the passport.
>
> Against this evidentiary backdrop, it is hard to see how DeChoudens's testimony regarding his decades-old recollection of the implausible nature of the answers that Doe gave in response to questions about the school that he attended in Puerto Rico could be thought to have had any material impact either on a juror's assessment that Doe's asserted biographical information was not what he had represented it to be or whether Doe knew that it was not. Nor does Doe offer any explanation of how it could have been, notwithstanding the problems he does not dispute existed with respect to the testimony of the sole witness he put forward and the evident strength of testimony (supported by documents) of Angel Rodriguez. Moreover, the only documentary evidence Doe introduced consisted of employment records that show only that he was using the name José Manuel Rodriguez and the social security number assigned to that person, neither of which is a fact in dispute.

Candidate window: `cl6105386:7`, `cl6105386:8`, `cl6105386:9`, `cl6105386:10`, `cl6105386:11`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl6105386:9']` | cl6105386:9 explains the proof required, that the testimony added little, and the overwhelming other evidence. |
| Rater B | `['cl6105386:9', 'cl6105386:10']` | cl6105386:9 says the government had to prove Doe's knowledge, the testimony added little, and other evidence including Angel Rodriguez and documents was overwhelming; cl6105386:10 says the testimony had no material impact given Angel's evident strength. |

**Recommended:** `['cl6105386:9', 'cl6105386:10']` — B: chunk 10 says the testimony had no material impact given the documented strength of Angel Rodriguez's testimony (points 2–3).

**Final label:** ______

---

### [ ] negligence_duty-qa-1 · qa_citation · Suquilanda v. Skyway Roofing, Inc. (mass, 2026-08-17)

Source: [https://www.courtlistener.com/opinion/10951829/suquilanda-v-skyway-roofing-inc/](https://www.courtlistener.com/opinion/10951829/suquilanda-v-skyway-roofing-inc/) · opinion 11419421 · cited authority as it appears: `Dilaveris v. W.T. Rich Co., 424 Mass. 9, 12 (1996)`

**Question:** In Suquilanda v. Skyway Roofing, what features did the Massachusetts Supreme Judicial Court say typically support a finding that a general contractor retained control of a subcontractor's safety practices?

**Reference notes:** Must mention: express contractual language assigning safety responsibility to the general contractor, concrete actions tied to those responsibilities, or both, as in Corsetti and Dilaveris.

**Chunks either rater chose:**

`cl11419421:5`

> to liability for physical harm to others for whose safety
>
> the employer owes a duty to exercise reasonable care, which
>
> is caused by his failure to exercise his control with
>
> reasonable care." The retained-control question "is [ordinarily] a question of fact for the jury." Corsetti, 396 Mass. at 11. Nevertheless, when the summary judgment record cannot support a finding of retained control as a matter of law, summary judgment is appropriate. See Lyon v. Morphew, 424 Mass. 828, 834-836 (1997) (affirming summary judgment where record was insufficient to establish retained control).
>
> Here, the motion judge concluded that the defendant did not "exercise any meaningful control over MBT's work, including the safety aspects of the work." The defendant's involvement was limited to delivering roof shingles, a boom lift, and a Dumpster -- none of which contributed to the fall -- and to visiting the site briefly on two occasions before the accident. During those visits, the defendant showed MBT which roof was to be replaced, checked whether additional materials were needed, and sought to ensure that MBT performed the work without damaging the property. On appeal, the plaintiff argues that the defendant retained control over the safety aspects of the work, citing language in the contract between the defendant and Jiminy Peak4 and the defendant's building permit application.
>
> Our cases finding sufficient retained control typically rest on express contractual language assigning safety responsibility to the general contractor, concrete actions tied

`cl11419421:6`

> 4 The motion judge did not address the contract between the defendant and Jiminy Peak as a basis for finding a duty of care. Because that contract is part of the summary judgment record, we consider it in our de novo review. See Roman v. Trustees of Tufts College, 461 Mass. 707, 711 (2012) (in our de novo review, we may affirm grant of summary judgment "on any ground supported by the record"). to those safety responsibilities, or both. In Corsetti, 396 Mass. at 11, the general contract required the general contractor to "initiate, maintain, and supervise all safety precautions and programs in connection with the Work," and the subcontract gave the general contractor "the authority and control necessary to carry out that responsibility." Id. Additionally, a site supervisor for the general contractor had authority to "direct subcontractors to remedy violations of safety rules and regulations and to stop work if they failed to comply," and he exercised that authority by "checking to see whether scaffolding was properly set" and discussing safety requirements and procedures with the subcontractor's foreman. Id. The supervisor also had actual knowledge that the subcontractor's employees "were not using safety belts while working on the scaffolding." Id.
>
> The pattern repeats in Dilaveris v. W.T. Rich Co., 424 Mass. 9, 12 (1996), where the general contract made the general contractor "solely responsible for all construction means, methods, techniques, sequences, and procedures," and further responsible for any failure to "take all proper precautions to protect persons from injury." Testimony confirmed that part of the general contractor's responsibilities "was to see that subcontractors followed safety procedures." Id.

Candidate window: `cl11419421:4`, `cl11419421:5`, `cl11419421:6`, `cl11419421:7`, `cl11419421:8`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl11419421:6']` | cl11419421:6 describes contract language and exercised authority in Corsetti and Dilaveris as the typical basis for retained control. |
| Rater B | `['cl11419421:5', 'cl11419421:6']` | The key sentence (express contractual language assigning safety responsibility, concrete actions tied to those responsibilities, or both) splits across cl11419421:5 and :6; :6 gives the Corsetti and Dilaveris examples. |

**Recommended:** `['cl11419421:5', 'cl11419421:6']` — B: the 'express contractual language … concrete actions' sentence splits across chunks 5–6 (§3.1 rule 3).

**Final label:** ______

---

### [ ] negligence_duty-qa-4 · qa_citation · Snay v. Burr (Slip Opinion) (ohio, 2021-11-24)

Source: [https://www.courtlistener.com/opinion/5300575/snay-v-burr-slip-opinion/](https://www.courtlistener.com/opinion/5300575/snay-v-burr-slip-opinion/) · opinion 5129137 · cited authority as it appears: `Turner v. Ohio Bell Tel. Co., 118 Ohio St.3d 215, 2008-Ohio-2010, 887 N.E.2d 1158`

**Question:** Why did the Ohio Supreme Court in Snay v. Burr reject the Snays' reading of Manufacturer's National Bank as imposing a broader duty on adjacent landowners than on political subdivisions?

**Reference notes:** Must mention: Manufacturer's involved an accident on the regularly traveled portion of the road; the court focused on an obstruction's effect on the safety of ordinary on-road travel for both the township and the occupier; so it did not recognize a duty for obstructions that do not affect ordinary travel.

**Chunks either rater chose:**

`cl5129137:10`

> {¶ 20} The Snays suggest that recognition of a duty under the facts of this case would not conflict with this court’s holding in Manufacturer’s, because, they contend, under the holding in Manufacturer’s, an adjacent landowner or an occupier of land adjacent to a public road owes a broader duty to motorists than does the political subdivision to which the road and right-of-way are dedicated. They argue that while this court limited the township’s duty to keeping the right-of-way free from any obstruction that “renders the regularly travelled portions of the highway unsafe for the usual and ordinary course of travel,” id., 63 Ohio St.3d 318, 587 N.E.2d 819, at paragraph one of the syllabus, we did not use similar limiting language with respect to the duty owed to motorists by the adjacent landowner or occupier of the adjacent land. Instead, the Snays posit, this court held that a landowner’s or occupier’s duty to a motorist arises from the landowner’s or occupier’s use of the right-of-way “in a manner that is inconsistent with a highway purpose, and where such usage constitutes an unreasonable hazard to the users of the highway,” id. at paragraph two of the syllabus. They maintain that “an unreasonable hazard to the users of the highway” encompasses an off-road hazard that a motorist might encounter upon veering off the road, even if the hazard does not endanger ordinary travel on the regularly traveled portion of the road. We disagree with the Snays’ reading of Manufacturer’s.
>
> {¶ 21} As the Snays concede, Manufacturer’s is factually different from this case because the accident in Manufacturer’s occurred on the regularly traveled portion of the road and in the ordinary course of travel through the intersection. Further, there was no dispute in Manufacturer’s that the corn growing in the right-of-way rendered ordinary travel on the road unsafe by obscuring motorists’

`cl5129137:11`

> SUPREME COURT OF OHIO visibility of cross-traffic, which ultimately resulted in the fatal crash. Because of those undisputed facts, there was no reason for the court to consider whether the occupier’s duty would also extend to an off-road condition that did not render ordinary travel on the road unsafe but which might present a hazard to a motorist who leaves the regularly traveled portion of the road. Review of the opinion in Manufacturer’s makes clear, however, that this court focused on an obstruction’s effect on the safety of ordinary on-road travel with respect to both the township’s duty to motorists and the duty owed by an occupier of adjacent land. See id. at 324 (“if the crops obstruct a driver’s vision in a way that creates a hazard to safe travel on the highway, the usage is inconsistent with the right-of-way’s purpose”). We therefore reject the Snays’ argument that this court’s holding in Manufacturer’s recognizes a duty to motorists owed by an adjacent landowner or an occupier of land adjacent to a public road with respect to obstructions in the right-of-way that do not affect the safety of ordinary travel on the road.
>
> {¶ 22} Since this court’s decision in Manufacturer’s, we have consistently considered the effect that an object or obstruction in a right-of-way has on the ordinary use of the roadway when determining the existence of duties owed to motorists. See, e.g., Turner v. Ohio Bell Tel. Co., 118 Ohio St.3d 215, 2008-Ohio-2010, 887 N.E.2d 1158; Link v. FirstEnergy Corp., 147 Ohio St.3d 285, 2016-Ohio-5083, 64 N.E.3d 965.

Candidate window: `cl5129137:9`, `cl5129137:10`, `cl5129137:11`, `cl5129137:12`, `cl5129137:13`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl5129137:11']` | cl5129137:11 explains Manufacturer's facts and its focus on ordinary on-road travel for both defendants. |
| Rater B | `['cl5129137:10', 'cl5129137:11']` | cl5129137:10 says Manufacturer's accident occurred on the regularly traveled portion; cl5129137:11 says the court focused on the obstruction's effect on ordinary on-road travel and rejects the Snays' reading. |

**Recommended:** `['cl5129137:10', 'cl5129137:11']` — B: chunk 10 (¶21) states the Manufacturer's accident occurred on the regularly traveled portion (point 1).

**Final label:** ______

---

### [ ] patent_obviousness-qa-5 · qa_citation · Virtek Vision International Ulc v. Assembly Guidance Systems, Inc. (cafc, 2024-03-27)

Source: [https://www.courtlistener.com/opinion/9488350/virtek-vision-international-ulc-v-assembly-guidance-systems-inc/](https://www.courtlistener.com/opinion/9488350/virtek-vision-international-ulc-v-assembly-guidance-systems-inc/) · opinion 9954963 · cited authority as it appears: `Belden Inc. v. Berk-Tek LLC, 805 F.3d 1064, 1073`

**Question:** Why did the Federal Circuit in Virtek Vision v. Assembly Guidance Systems reverse the Board's finding of a motivation to combine Keitler and Briggs?

**Reference notes:** Must mention: recognizing that two alternative arrangements (a one-camera angular system and a two-camera 3D coordinate system) were both known in the art does not satisfy motivation to combine; Briggs disclosed both options but gave no reason to use 3D coordinates instead of angular directions; obviousness asks whether a skilled artisan would have been motivated to make the combination, not merely could have.

**Chunks either rater chose:**

`cl9954963:4`

> We conclude that the Board erred as a matter of law with regard to the motivation to combine. It does not suf-fice to meet the motivation to combine requirement to rec-ognize that two alternative arrangements such as an angular direction system using a single camera and a 3D coordinate system using two cameras were both known in the art. Briggs discloses a laser projector system with dif-ferent embodiments of laser tracker systems—one that uses two cameras to determine the 3D coordinates of a tar-get, J.A. 757 ¶ 49, and another that uses one camera to de-termine angular measurements of a target, J.A. 758 ¶ 51. Briggs discloses these two measurement options “may be applied to any computer controlled aiming system.” J.A. 6 VIRTEK VISION INTERNATIONAL ULC v.
>
> ASSEMBLY GUIDANCE SYSTEMS, INC. 754 ¶ 42. These disclosures, however, do not provide any reason why a skilled artisan would use 3D coordinates in-stead of angular directions in a system. See Belden Inc. v. Berk-Tek LLC, 805 F.3d 1064, 1073 (Fed. Cir. 2015) (“[O]bviousness concerns whether a skilled artisan not only could have made but would have been motivated to make the combinations or modifications of prior art to arrive at the claimed invention.”).

`cl9954963:5`

> The mere fact that these possible arrangements existed in the prior art does not provide a reason that a skilled ar-tisan would have substituted the one-camera angular di-rection system in Keitler and Bridges with the two-camera 3D coordinate system disclosed in Briggs. There was no argument in the petition regarding why a skilled artisan would make this substitution—other than that the two dif-ferent coordinate systems were “known to be used.” J.A. 194–96, 214–16. The petition does not argue Briggs articulates any reason to substitute one for another or any advantages that would flow from doing so. Nor does Dr. Mohazzab, Aligned Vision’s expert, articulate any reason why a skilled artisan would combine these references. In his declaration, he testified “it would have been obvious” to use the 3D coordinates instead of angular measurements because “both such measurement systems were known.” J.A. 815 ¶ 51; J.A. 837 ¶ 93. 1 Moreover, he stated eleven
>
> 1 The parties appear to dispute whether the Board relied on Dr. Mohazzab’s declaration in support of its moti-vation to combine findings. See Oral Arg. at 3:31–4:50, 13:38–57, 23:55–24:57, https://oralarguments.cafc.uscourt s.gov/default.aspx?fl=22-1998_12052023.mp3. The Board explained that its motivation to combine findings were based on “the support provided in the Petition.” Decision, 2022 WL 1463734, at *9 (citing J.A. 194–96); id. at *19 (cit-ing J.A. 210, 215–16). There is no dispute the petition re-lied upon Dr. Mohazzab’s declaration. J.A. 194–96, 210, 215–16; Oral Arg. at 4:12–20. VIRTEK VISION INTERNATIONAL ULC v. 7 ASSEMBLY GUIDANCE SYSTEMS, INC. times that he did not provide any reason to combine the references in his expert declaration. See Mohazzab Dep. Tr. at 53:15–20 (testifying “I’m not sure I can find” a reason to combine Briggs and Keitler in declaration), 89:24–90:5 (testifying “I do not state any reasons” to combine Bridges and Briggs in declaration), 56:6–10, 59:25–60:21, 62:1–5, 62:12–16, 64:1–11, 65:4–11, 88:25–89:4, 91:19–24, 93:9–14; cf. id. at 55:15–17 (testifying “[y]ou don’t have to combine” Keitler and Briggs), 88:11–89:15 (testifying Briggs “[d]oesn’t need to be combined” with Bridges). 2

`cl9954963:6`

> KSR provides an important understanding of the cir-cumstances in which limitations from different references can be combined to conclude that a claimed invention would have been obvious. In KSR, the Supreme Court ex-plained, “[w]hen there is a design need or market pressure to solve a problem and there are a finite number of identi-fied, predictable solutions, a person of ordinary skill has good reason to pursue the known options within his or her technical grasp.” KSR Int’l Co. v. Teleflex Inc., 550 U.S. 398, 421 (2007). “If this leads to the anticipated success, it is likely the product not of innovation but of ordinary skill and common sense.” Id. KSR did not do away with the requirement that there must exist a motivation to combine various prior art references in order for a skilled artisan to make the claimed invention.
>
> 2 Virtek appeals the Board’s denial of its motion to exclude Dr. Mohazzab’s expert declaration. We need not decide whether the Board abused its discretion in declining to exclude the declaration because the conclusory asser-tions in Dr. Mohazzab’s declaration do not provide substan-tial evidence for finding a motivation to combine. 8 VIRTEK VISION INTERNATIONAL ULC v.
>
> ASSEMBLY GUIDANCE SYSTEMS, INC.
>
> Here, there was no argument about common sense in the petition or in Dr. Mohazzab’s declaration. 3 See J.A. 194–96, 214–16; J.A. 815 ¶ 51; J.A. 837 ¶ 93. There was no evidence that there are a finite number of identi-fied, predictable solutions. There is no evidence of a design need or market pressure. In short, this case involves noth-ing other than an assertion that because two coordinate systems were disclosed in a prior art reference and were therefore “known,” that satisfies the motivation to combine analysis. That is an error as a matter of law. It does not suffice to simply be known. A reason for combining must exist.

Candidate window: `cl9954963:2`, `cl9954963:3`, `cl9954963:4`, `cl9954963:5`, `cl9954963:6`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl9954963:4']` | cl9954963:4 states the Board's legal error, Briggs's lack of any reason to choose one system, and the would-have-been-motivated standard from Belden. |
| Rater B | `['cl9954963:4', 'cl9954963:5', 'cl9954963:6']` | Chunk 4 states known alternatives do not satisfy motivation and Briggs gave no reason to use 3D over angular; chunks 5 and 6 restate that mere existence/being known gives no reason and a reason for combining must exist. |

**Recommended:** `['cl9954963:4', 'cl9954963:5']` — Partly B: chunk 5 says the mere existence of both arrangements gives no reason to substitute (points 1–2); chunk 6 is about KSR generally, not the would-vs-could point.

**Final label:** ______

---

### [ ] personal_jurisdiction-qa-2 · qa_citation · Rios v. Bayer Corp. (ill, 2020-06-04)

Source: [https://www.courtlistener.com/opinion/4758410/rios-v-bayer-corp/](https://www.courtlistener.com/opinion/4758410/rios-v-bayer-corp/) · opinion 4538757 · cited authority as it appears: `Moore v. Bayer Corp., No. 4:18 CV 262 CDP, 2018 WL 4144795, at *1`

**Question:** What did the Illinois Supreme Court hold in Rios v. Bayer Corp. about specific personal jurisdiction over the defendant for the claims of out-of-state plaintiffs?

**Reference notes:** Must mention: the nonresident plaintiffs identified no jurisdictionally relevant link between their claims and Illinois (devices not implanted there, physicians not trained there, no warnings received there); where there is no adequate link, Illinois lacks specific jurisdiction as to those claims; plaintiffs failed to establish a prima facie basis.

**Chunks either rater chose:**

`cl4538757:9`

> California. Id. at ___, 137 S. Ct. at 1781. “The mere fact that other plaintiffs were prescribed, obtained, and ingested [the drug] in California—and allegedly sustained the same injuries as did the nonresidents—does not allow the State to assert specific jurisdiction over the nonresidents’ claims.” (Emphasis in original.) Id at ___, 137 S. Ct. at 1781. The Court also found that its decision would “not result in the parade of horribles that respondents conjure up.” Id. at ___, 137 S. Ct. at 1783. The Court noted that the out-of-state plaintiffs could pursue their claims elsewhere, including by joining in a consolidated action in states that had general jurisdiction over defendant. Id. at ___, 137 S. Ct. at 1783. ¶ 24 As was true in Bristol-Myers, in this case, defendants do not dispute that they purposefully directed activities toward Illinois. Bayer conducted clinical trials in Illinois (as well as various other states), held a physician training program for Essure, and coordinated a marketing strategy in Illinois. Yet, the question here is whether the nonresident plaintiffs’ claims arise out of, or relate to, those activities in any meaningful sense of the terms. We find that they do not. ¶ 25 For example, plaintiffs allege that Bayer failed to establish and maintain procedures to confirm that Essure devices were properly manufactured, and they assert that the manufacturing defects caused their harm. According to plaintiffs, Essure initially was manufactured at Conceptus’s manufacturing facility in San Carlos, California. They also allege that Conceptus had manufacturing sites for Essure in Chihuahua, Mexico, and Juarez, Mexico. Then in June 2015, according to plaintiffs, the FDA approved a manufacturing site for Bayer in Heredia, Costa Rica. Conspicuously absent from plaintiffs’ allegations, however, is any assertion that their Essure devices were manufactured in Illinois or that Bayer did, or should have, established manufacturing procedures in Illinois. Without such allegations, there is no adequate link between the nonresident plaintiffs’ manufacturing defect claims and this forum. ¶ 26 Plaintiffs also allege that Bayer “willfull[y] disseminated false and misleading information [about Essure] at a time when they knew or should have known

`cl4538757:10`

> there were no reasonable grounds for believing these claims to be true.” Yet plaintiffs fail to allege that either they or their physicians received that false information in Illinois, and as noted, these plaintiffs and their physicians do not reside in this forum. According to plaintiffs, Bayer also “failed to warn Plaintiffs and their physicians by not reporting the risk of serious defects and life-altering complications described herein that Defendants knew or should have known were associated with Essure prior to the time of Plaintiffs’ implantation.” However, the nonresident plaintiffs’ devices were not implanted in Illinois. 3 And nothing in their

`cl4538757:11`

> For example, one allegation noted that a nonresident plaintiff “was implanted with Essure on July 7, 2010 in Colorado Springs, CO by Dr. Christopher S. Russell”; another alleges a nonresident plaintiff “was implanted with Essure in 2010 in Knoxville, TN by Turkey Creek Medical Center.” A third alleges a nonresident plaintiff was “implanted with Essure in 2011 in Galveston, TX at UTMB Galveston.” complaints links Bayer’s alleged failure to warn the nonresidents and their physicians to any activities that occurred or should have occurred in Illinois. ¶ 27 Finally, plaintiffs allege that Bayer “undertook a duty of training physicians, including the implanting physician, on how to properly use (1) its own mechanism of delivery and (2) the specialized hysteroscopic equipment manufactured by a third party.” In their view, defendants breached their duty to properly train physicians. However, the nonresident plaintiffs do not allege that Bayer trained their physicians in Illinois, and again, the nonresidents’ devices were not implanted in Illinois. ¶ 28 In short, the nonresident plaintiffs have identified no jurisdictionally relevant links between their claims and Illinois. See Bristol-Myers, 582 U.S. at ___, 137 S. Ct. at 1782 (requiring a “connection between the nonresidents’ claims and the forum”); see also Moore v. Bayer Corp., No. 4:18 CV 262 CDP, 2018 WL 4144795, at *1 (E.D. Mo. Aug. 29, 2018) (“As many judges in this district have found when considering the same issues involving Bayer and Essure in Missouri, the connections between Missouri and the non-Missouri plaintiffs’ claims against Bayer are too attenuated for this court to exercise personal jurisdiction over Bayer.”). Where no adequate link exists between Illinois and the nonresident plaintiffs’ claims, it necessarily follows that Illinois lacks specific personal jurisdiction over defendants as to those claims. For these reasons, we hold that plaintiffs failed to meet their burden of establishing a prima facie basis to exercise specific personal jurisdiction over defendants as to the nonresident plaintiffs’ claims. ¶ 29 Plaintiffs direct our attention to Walden v. Fiore, 571 U.S. 277, 284 (2014), insisting that our personal jurisdiction inquiry must “focus[ ] on the relationship among the defendant,

`cl4538757:13`

> omitted.) Bristol-Myers, 582 U.S. at ___, 137 S. Ct. at 1780-81. ¶ 31 These factors weigh strongly against Illinois courts exercising specific personal jurisdiction over defendants for the out-of-state plaintiffs’ claims. Illinois has no particular interest in resolving claims that did not arise out of or relate to activities that occurred here. Plaintiffs’ interest in obtaining relief also does not weigh in favor of Illinois courts’ exercise of specific personal jurisdiction as to non-Illinois plaintiffs. The nonresidents have not explained how Illinois could be a convenient location for this litigation when they were not implanted with their devices here and have identified no other activity that would connect their specific claims to Illinois. Further, defendants assert—and plaintiffs have not disputed—that many nonresident plaintiffs initiated duplicate actions in California, which demonstrates that the interests of judicial economy are not furthered by permitting their claims to proceed in Illinois. ¶ 32 In concluding that jurisdiction was proper, the courts below relied heavily on M.M., 2016 IL App (1st) 151909. We note that M.M. was decided nearly one year before Bristol-Myers. As such, the appellate court did not have the benefit of the Supreme Court’s additional guidance on the propriety of exercising specific personal jurisdiction under similar circumstances. Bristol-Myers has clarified that “[a] corporation’s continuous activity of some sorts within a state . . . is not enough to support the demand that the corporation be amenable to suits unrelated to that activity.” (Internal quotation marks omitted.) Bristol-Myers, 582 U.S. at ___, 137 S. Ct. at 1781. The Court explained that the fact that in-state plaintiffs allegedly sustained the same injuries from a drug as did nonresidents does not allow a state to assert specific personal jurisdiction over the nonresidents’ claims. Id. at ___, 137 S. Ct. at 1781. We therefore hold that M.M. does not reflect the law in Illinois and should no longer be relied upon. ¶ 33 CONCLUSION ¶ 34 In sum, we conclude that the nonresident plaintiffs’ claims did not arise out of or relate to defendants’ in-state activities and, thus, Illinois courts lack specific personal jurisdiction over Bayer

Candidate window: `cl4538757:9`, `cl4538757:10`, `cl4538757:11`, `cl4538757:12`, `cl4538757:13`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl4538757:11']` | cl4538757:11 states the nonresidents' devices were not implanted in Illinois and their physicians were not trained there, concludes there is no adequate link and no specific jurisdiction, and says plaintiffs failed their prima facie burden. |
| Rater B | `['cl4538757:9', 'cl4538757:10', 'cl4538757:11', 'cl4538757:13']` | Chunks 10-11 state devices not implanted, no false info received, no training in Illinois, no jurisdictionally relevant links and the prima facie holding; chunk 9 finds no adequate link for manufacturing claims; chunk 13 concludes Illinois lacks specific jurisdiction. |

**Recommended:** `['cl4538757:10', 'cl4538757:11', 'cl4538757:13']` — Partly B: chunk 10 (devices not implanted, no false info received in Illinois) and chunk 13 (no connection; factors weigh against jurisdiction) state points 1–2; chunk 9 states the general no-relation finding but none of the listed links.

**Final label:** ______

---

### [ ] title_vii_retaliation-qa-4 · qa_citation · Stella Paterakos v. City of Chicago (ca7, 2025-08-12)

Source: [https://www.courtlistener.com/opinion/10652248/stella-paterakos-v-city-of-chicago/](https://www.courtlistener.com/opinion/10652248/stella-paterakos-v-city-of-chicago/) · opinion 11118835 · cited authority as it appears: `Ellis v. CCA of Tennessee LLC, 650 F.3d 640, 650 (7th Cir. 2011)`

**Question:** Why did the Seventh Circuit in Paterakos v. City of Chicago conclude that a one-week assignment to a second call center was not an adverse employment action even under the Muldrow standard?

**Reference notes:** Must mention: Muldrow does not require significant harm but the plaintiff must show some harm; the assignment did not reduce responsibilities, pay or benefits; the half-hour shift change and new location were minor and caused no objective harm.

**Chunks either rater chose:**

`cl11118835:10`

> Paterakos argues that her one-week assignment to the De-Paul Center was an adverse employment action because it changed her working hours and oﬃce location. An “adverse employment action is some quantitative or qualitative change in the terms or conditions of [the plaintiﬀ’s] employment that is more than a mere subjective preference.” Madlock v. WEC Energy Group, Inc., 885 F.3d 465, 470 (7th Cir. 2018) (internal quotation marks omitted), quoting Johnson v. Cambridge Indus-tries, Inc., 325 F.3d 892, 901 (7th Cir. 2003). The words “terms” and “conditions” cover more than economic or tangible inju-ries. Meritor Savings Bank, FSB v. Vinson, 477 U.S. 57, 64 (1986). They also encompass harm to an employee’s “career pro-spects” and “humiliating, degrading, unsafe, unhealthy” or otherwise negative changes to an employee’s work condi-tions. Madlock, 885 F.3d at 470, quoting Boss v. Castro, 816 F.3d 910, 917 (7th Cir. 2016). Yet not every change “that makes an employee unhappy is an actionable adverse action.” Id. at 470, quoting Nichols v. Southern Illinois Univ.-Edwardsville, 510 F.3d 772, 780 (7th Cir. 2007). The district court concluded that Paterakos’s one-week as-signment to the DePaul Center was not an adverse employ-ment action because she had not identiﬁed “any signiﬁcant disadvantage she experienced due to the temporary change in reporting location.” The court applied the standard under then-controlling circuit precedent. See Boss, 816 F.3d at 917. That standard was modiﬁed in Muldrow v. City of St. Louis, 601 U.S. 346 (2024), where the Supreme Court clariﬁed that a Title circumstances requirement and Paterakos has abandoned the McDonnell Douglas framework on appeal, Ames does not affect this decision. 12 No. 24-1567 VII plaintiﬀ identifying a job transfer as an adverse employ-ment action must still show “some harm respecting an iden-tiﬁable term or condition of employment.” Id. at 355. Under Muldrow, however, transferees need not show that the harm incurred was “signiﬁcant,” or “serious, or substantial, or any similar adjective suggesting that the disadvantage to the em-ployee must exceed a heightened bar.” Id. (internal quotation marks omitted), quoting Muldrow v. City of St. Louis, 30 F.4th 680, 688 (8th Cir. 2022).

`cl11118835:11`

> Even under Muldrow, though, we agree with the district court that the one-week assignment to the DePaul Center to enable social distancing in the earliest stages of the pandemic did not constitute an adverse employment action. Although Paterakos’s failure to show “signiﬁcant” harm from the brief assignment to the DePaul Center is not necessarily decisive, her failure to show that she suﬀered any harm is. The assign-ment did not diminish Paterakos’s job responsibilities, com-pensation, or beneﬁts or make her otherwise worse oﬀ. While it shifted Paterakos’s working hours by half an hour and re-quired her to report to a diﬀerent location, Paterakos has not identiﬁed any way that either of these minor changes in her working conditions objectively harmed her. See Ellis v. CCA of Tennessee LLC, 650 F.3d 640, 650 (7th Cir. 2011) (aﬃrming grant of summary judgment for employer in Title VII action: “A change in shift assignments will not normally be suﬃcient to qualify as an adverse employment action, unless it is ac-companied by some other detriment.”). The brief assignment to the DePaul Center did not rise to the level of an adverse employment action that could support a Title VII claim. No. 24-1567 13
>
> 2. Pretext
>
> Federal employment discrimination laws do not limit their protection to perfect employees. An employer can vio-late those laws by imposing discriminatory discipline, penal-izing employees diﬀerently for comparable poor performance or misconduct based on their race, sex, national origin, age, disability, or other protected status. See, e.g., Morris v. BNSF Railway Co., 969 F.3d 753, 758 (7th Cir. 2020); Caskey v. Colgate-Palmolive Co., 535 F.3d 585, 592 (7th Cir. 2008). Paterakos ar-gues that defendants’ performance-based rationales for the three suspensions were mere pretexts for racial discrimina-tion. Evidence of pretext can be circumstantial evidence of un-lawful motives under the broader Ortiz test. E.g., Murphy v. Caterpillar Inc., 140 F.4th 900, 911–12 (7th Cir. 2025); Vassileva v. City of Chicago, 118 F.4th 869, 874 (7th Cir. 2024). One way to show pretext and thus discrimination can be an employer’s failure to take comparable action against other employees for similar poor performance or misconduct.

Candidate window: `cl11118835:9`, `cl11118835:10`, `cl11118835:11`, `cl11118835:12`, `cl11118835:13`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl11118835:11']` | cl11118835:11 holds no harm was shown, cites the unchanged pay and duties, and treats the minor shift and location changes as insufficient. |
| Rater B | `['cl11118835:10', 'cl11118835:11']` | cl11118835:11 says no harm shown, no reduction in responsibilities, pay or benefits, and the half-hour and location changes were minor; cl11118835:10 states Muldrow requires some harm but not significant harm. |

**Recommended:** `['cl11118835:10', 'cl11118835:11']` — B: chunk 10 states Muldrow requires some harm but not significant harm (point 1).

**Final label:** ______

---

## Random 10% audit of agreed items (13)

### [ ] agency_arbitrary_capricious-cc-2 · citation_check · Shenzhen Youme v. FDA (ca5, 2025-08-06)

Source: [https://www.courtlistener.com/opinion/10649060/shenzhen-youme-v-fda/](https://www.courtlistener.com/opinion/10649060/shenzhen-youme-v-fda/) · opinion 11115647 · cited authority as it appears: `Wages & White Lion Invs., L.L.C. v. FDA, 90 F.4th 357 (5th Cir. 2024) (en banc)`

**Claim:** FDA's statement that Youme's study suggested its products might reinforce addiction among current smokers was not a new evidentiary requirement, because the statute already directs FDA to consider whether existing users will stop using tobacco products.

**Cited passage:** `cl11115647:10`

> The same is true for Youme’s argument that FDA changed its position, or imposed a new evidentiary requirement, when it stated that Youme’s “own key study . . . appears to show that subjective effects experienced from use of the new products may reinforce adults who smoke” with “only a moderate chance that some current [combustible-cigarette] users would switch completely to the new product.” This is not a new requirement. The TCA requires FDA to consider “the increased or decreased likelihood that existing users of tobacco products will stop using such products.” 21 U.S.C. § 387j(c)(4)(A). A product’s potential to reinforce nicotine addiction in those who currently use combustible cigarettes is precisely the inquiry FDA is to make to determine whether a product is appropriate for the protection of the public health. FDA used slightly different language but the “distinction amounts to splitting hairs.” See Fontem, 82 F.4th at 1216. The denial was reasonable and reasonably explained.
>
> Youme also asserts that the gaps in information resulted from new evidentiary requirements FDA imposed “after the fact,” with Youme having no opportunity to satisfy those requirements. Specifically, Youme contends FDA shifted its requirements from “testing of the device with a ‘reasonable range of available e-liquids’ to e-liquids that represent ‘the highest and lowest nicotine concentrations’ available on the market,” thereby moving the regulatory goalposts. Youme contends this change is “exactly the sort of moving of the regulatory goalposts” found to be arbitrary
>
> No. 24-60060 and capricious in Wages & White Lion Invs., L.L.C. v. FDA, 90 F.4th 357 (5th Cir. 2024) (en banc) vacated, 145 S. Ct. 898 (2025).

<details><summary>Other passages available</summary>

`cl9379438:6`

> Perhaps these contentions have merit; maybe they do not. But unfor-tunately for the FRA, “[a]n agency’s action must be upheld, if at all, on the basis articulated by the agency itself,” Texas, 40 F.4th at 226–27, and here, the agency has barely articulated any basis at all. The paucity of reasoning is especially glaring in the face of the agency’s statutory mandate to prioritize safety. BNSF has made evidence-based claims that ATI is safer and more efficient than visual inspection alone. The implementation of ATI pursuant to the prior waiver appears to have been an unqualified success. The FRA is thus duty-bound to provide further justification for its rejection of the tech-nology’s expansion.
>
> We reiterate: “[A]gency action [must] be reasonable and reasonably explained.” Prometheus Radio Project, 141 S. Ct. at 1158. The agency must “articulate a satisfactory explanation for its action including a ‘rational con-nection between the facts found and the choice made.’” Motor Vehicle Mfrs., 463 U.S. at 43 (quoting Burlington Truck Lines, 371 U.S. at 168). Finding the FRA’s letter lacking in this regard, we GRANT review, VACATE, and REMAND for reconsideration. This is a limited remand; this panel retains jurisdiction. We direct the FRA to enter its decision no later than one hun-dred days from the announcement of this opinion.
>
> An agency must “provide a reasoned explanation for the change,” “at least ‘dis-play awareness that it is changing position[,]’ and ‘show that there are good reasons for the new policy.’” Encino Motorcars, LLC v. Navarro, 579 U.S. 211, 221 (2016) (quoting FCC v. Fox Television Stations, Inc., 556 U.S. 502, 515 (2009)). When reliance interests have been engendered by an existing policy, “an ‘[u]nexplained inconsistency’ in agency policy is ‘a reason for holding [a decision] to be an arbitrary and capricious change from agency practice.’” Id. (quoting Nat’l Cable & Telecomms. Ass’n v. Brand X Internet Servs., 545 U.S. 967, 981 (2005)).

`cl11115647:7`

> No. 24-60060 of the tobacco product,” considering both “the increased or decreased likelihood that existing users of tobacco products will stop using such products[,] and the increased or decreased likelihood that those who do not use tobacco products will start using such products.” § 387j(c)(4)(A)–(B). The burden is on the applicant to make the appropriate showing by including all relevant information necessary to make that determination in its initial application. § 387j(b)(1)(A)–(G). Based on the application, FDA makes a “single predictive judgment whether a given tobacco product, on balance, will benefit the public as a whole.” Fontem US, LLC v. FDA, 82 F.4th 1207, 1215 (D.C. Cir. 2023). When the application lacks evidence to support a showing that its product “will benefit the public as a whole,” the application must be denied. Id.; § 387j(c)(2)(A). I. FDA’s Failure to Weigh
>
> Youme contends that FDA failed to weigh the overall risks and benefits of its product, rendering its denial arbitrary and capricious. In particular, Youme asserts that FDA did not consider Youme’s “extensive evidence of the potential public health benefits of its products.” Instead, FDA found gaps in data caused by the imposition of new evidentiary requirements “after the fact” and then refused to allow Youme to satisfy those requirements.3 They contend that, like in Fontem, FDA in this case failed to consider the evidence of potential benefits of the devices. See Fontem, 82 F.4th 1207. We examine that authority.
>
> Fontem submitted applications for both flavored and unflavored products. Id. at 1211. The court approved the denial of the marketing
>
> _____________________
>
> 3 Youme also contends that data submitted two weeks after the submission deadline satisfied the alleged new requirement, but that FDA acted arbitrarily and capriciously by refusing to weigh those benefits. We view this to be an argument that FDA’s deadline is arbitrary and capricious, so we address this argument in Section II of the opinion.

`cl11115647:9`

> In this record, though, there is evidence that FDA expressly considered the potential benefits. A few examples: “ENDS carry the potential to positively impact population health when used as an alternative to combusted tobacco,” “abuse liability of the new products is lower than that of a [combustible cigarette] when used with [certain nicotine concentrations],” and “[s]hould adults who currently use [combustible cigarettes] switch exclusively to use of the new products, they are likely to maintain similar or slightly lower nicotine dependence levels.”
>
> FDA evaluated that evidence, found it insufficient, and explained how the specific deficiencies related to its overall conclusion that Youme failed to show its products were appropriate for the protection of the public health. It explained that high nicotine content e-liquids are prevalent on the market and Youme failed to provide sufficient data to evaluate the risks associated with use of the new products with those high concentration liquids. FDA explained that abuse liability “indicates the degree to which users of the new products are likely to use and develop an addiction to the product and face the health risks posed by long term product use.” FDA also explained that “high abuse liability may increase the likelihood that tobacco users and nonusers, including youth, who try the new product for the first time will continue using it.” FDA asserts that Youme’s evidence of potential public-health benefits depends on existing smokers transitioning away from combustible cigarettes. FDA found “only a moderate chance that some current [combustible-cigarette] users would switch completely to the new products.”
>
> Here, unlike in Fontem, FDA provided meaningful explanations of the importance of determining a product’s abuse liability and the relevance of that information to the statutory public-health inquiry. FDA weighed the abuse-liability risk with the “evidence that Youme’s products would help existing tobacco users quit or substantially reduce their use of combustible
>
> No. 24-60060 cigarettes.” FDA determined that “additional information on abuse liability, or on the likelihood that consumers would follow” product recommendations was necessary to prove the products were appropriate for the protection of the public health. The decision was reasonable and reasonably explained.

`cl9915536:8`

> At the time, the agency explained that changes to the healthcare system since the adoption of the prior regulations in 1991, along with the agency’s long experience in adjudicating disability claims, showed that “supportability” and “consistency” were the two most important factors for evaluating medical opinions. Id. at 5853. “Many individuals receive health care from multiple medical sources,” the agency explained, “such as from coordinated and managed care organizations,” and “less frequently develop a sustained relationship with one treating physician.” Id. Supportability and consistency, according to the agency, are therefore “more objective measures that will foster the fairness and efficiency in [its] administrative process.” Id. Moreover, the agency expressed concern that, under the former rule, courts “focused more on whether [the agency] sufficiently articulated the weight [it] gave treating source opinions, rather than on whether substantial evidence support[ed]” the agency’s “final decision.” Id. Still, the agency noted, the regulations “retain the relationship between the medical source and the claimant as one of the factors” to consider. Id.
>
> The Eleventh Circuit recently held these regulations to be valid under the APA based on the agency’s reasoned explanation that the regulations “help[] to ‘eliminate confusion about a hierarchy of medical sources’ that no longer reflects how most claimants receive health care.” Harner v. Soc. Sec. Admin., Comm’r, 38 F.4th 892, 897 (11th Cir. 2022) (quoting Revisions to Rules Regarding the Evaluation of Medical Evidence, 82 Fed. Reg. at 5853) (evaluating 20 C.F.R. § 404.1520c). We agree. The agency’s response to public comment and reasoned explanation for the regulatory changes establishes that the regulations are not arbitrary or capricious. We join the Eleventh Circuit in holding that the regulations are valid under the APA.
>
> CONCLUSION
>
> The Social Security Administration’s 2017 medical-evidence regulations fall within the broad scope of the Commissioner’s authority under the Social Security Act, and the agency provided a reasoned explanation for the regulatory changes, making the regulations neither arbitrary nor capricious under the APA.
>
> AFFIRMED.

</details>

| | Label | Reason |
|---|---|---|
| Rater A | `supported` | Step 1: cl11115647:10 says 'This is not a new requirement' because the TCA requires FDA to consider the likelihood existing users will stop, and a product's potential to reinforce nicotine addiction is 'precisely the inquiry FDA is to make'. |
| Rater B | `supported` | cl11115647:10 says this is not a new requirement because the TCA requires FDA to consider whether existing users will stop using such products. |

**Recommended:** `supported` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] agency_arbitrary_capricious-qa-5 · qa_citation · Juanita Cross v. Martin O'Malley (ca9, 2024-01-05)

Source: [https://www.courtlistener.com/opinion/9457711/juanita-cross-v-martin-omalley/](https://www.courtlistener.com/opinion/9457711/juanita-cross-v-martin-omalley/) · opinion 9915536 · cited authority as it appears: `Harner v. Soc. Sec. Admin., Comm’r, 38 F.4th 892, 897 (11th Cir. 2022)`

**Question:** Why did the Ninth Circuit in Cross v. O'Malley conclude that the 2017 medical-evidence regulations were not arbitrary or capricious under the APA?

**Reference notes:** Must mention: the agency explained that changes in how people receive health care and its adjudication experience made supportability and consistency the most important and more objective factors; the regulations kept the claimant relationship as a factor; the court joined the Eleventh Circuit in finding the explanation and response to comments sufficient.

**Chunks either rater chose:**

`cl9915536:8`

> At the time, the agency explained that changes to the healthcare system since the adoption of the prior regulations in 1991, along with the agency’s long experience in adjudicating disability claims, showed that “supportability” and “consistency” were the two most important factors for evaluating medical opinions. Id. at 5853. “Many individuals receive health care from multiple medical sources,” the agency explained, “such as from coordinated and managed care organizations,” and “less frequently develop a sustained relationship with one treating physician.” Id. Supportability and consistency, according to the agency, are therefore “more objective measures that will foster the fairness and efficiency in [its] administrative process.” Id. Moreover, the agency expressed concern that, under the former rule, courts “focused more on whether [the agency] sufficiently articulated the weight [it] gave treating source opinions, rather than on whether substantial evidence support[ed]” the agency’s “final decision.” Id. Still, the agency noted, the regulations “retain the relationship between the medical source and the claimant as one of the factors” to consider. Id.
>
> The Eleventh Circuit recently held these regulations to be valid under the APA based on the agency’s reasoned explanation that the regulations “help[] to ‘eliminate confusion about a hierarchy of medical sources’ that no longer reflects how most claimants receive health care.” Harner v. Soc. Sec. Admin., Comm’r, 38 F.4th 892, 897 (11th Cir. 2022) (quoting Revisions to Rules Regarding the Evaluation of Medical Evidence, 82 Fed. Reg. at 5853) (evaluating 20 C.F.R. § 404.1520c). We agree. The agency’s response to public comment and reasoned explanation for the regulatory changes establishes that the regulations are not arbitrary or capricious. We join the Eleventh Circuit in holding that the regulations are valid under the APA.
>
> CONCLUSION
>
> The Social Security Administration’s 2017 medical-evidence regulations fall within the broad scope of the Commissioner’s authority under the Social Security Act, and the agency provided a reasoned explanation for the regulatory changes, making the regulations neither arbitrary nor capricious under the APA.
>
> AFFIRMED.

Candidate window: `cl9915536:4`, `cl9915536:5`, `cl9915536:6`, `cl9915536:7`, `cl9915536:8`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl9915536:8']` | cl9915536:8 recounts the agency's reasons and holds the regulations valid under the APA. |
| Rater B | `['cl9915536:8']` | cl9915536:8 gives the agency's explanation (healthcare changes, supportability and consistency as objective factors), retention of the relationship factor, and joining the Eleventh Circuit. |

**Recommended:** `['cl9915536:8']` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] contract_interpretation-cc-5 · citation_check · Privilege Underwriters Reciprocal Exchange v. Jeff Mankoff and Staci Mankoff (tex, 2026-02-13)

Source: [https://www.courtlistener.com/opinion/10793200/privilege-underwriters-reciprocal-exchange-v-jeff-mankoff-and-staci/](https://www.courtlistener.com/opinion/10793200/privilege-underwriters-reciprocal-exchange-v-jeff-mankoff-and-staci/) · opinion 11259842 · cited authority as it appears: `EBS Sols., Inc. v. Hegar, 601 S.W.3d 744, 758 (Tex. 2020)`

**Claim:** Lists in the Insurance and Property Codes that name tornadoes and windstorms separately do not show that 'windstorm' ordinarily excludes a tornado, because such lists pair broad terms with narrower ones.

**Cited passage:** `cl11259842:7`

> Considering the use of the term “windstorm” in statutes does not call that conclusion into question. See Tex. State Bd. of Exam’rs of Marriage & Fam. Therapists, 511 S.W.3d at 35. Neither the Insurance Code nor the Property Code defines “ windstorm” or “tornado.” See Pharr- San Juan-Alamo Indep. Sch. Dist. v. Tex. Pol. Subdivision Prop./Cas. Joint Self Ins. Fund, 642 S.W.3d 466, 474– 76 (Tex. 2022) (explaining how several statutes defined the term at issue, as well as related terms, and therefore provided guidance on ordinary meaning). Various sections of the Insurance Code and one section of the Property Code, however, list tornadoes and windstorms separately. Insureds contend that this indicates an ordinary meaning of “windstorm” that excludes a tornado. We disagree.
>
> The provisions at issue include broad enumerated terms with ordinary meanings that encompass accompanying narrower terms. See, e.g., TEX. INS. CODE § 252.003 (including terms such as “rain,” “tornado,” and “lightning” in a list that also includes “weather or climatic conditions”); see also id. §§ 542A.001(2)(C), 1806.102(c)(12)(A); TEX. PROP. CODE § 92.0562; TEX. INS. CODE art. 5.13(c). We have recognized that the Legislature may repeat itself for emphasis, see In re City of Georgetown, 53 S.W.3d 328, 336 (Tex. 2001), and nothing in the cited provisions suggests that the lists confer an ordinary meaning that categorically excludes the narrower terms from the broader ones, see EBS Sols., Inc. v. Hegar, 601 S.W.3d 744, 758 (Tex. 2020) (“Normally, when a term within a statute is susceptible to either a broad or a narrow meaning, we will presume that the broader meaning of the term is intended, being sensitive to the term’s context in the statute.”). There is not a narrowing modifier in any of the provisions to indicate that the Legislature understood “windstorm” to exclude a tornado. See generally Cadena Comercial USA Corp. v. Tex. Alcoholic Beverage Comm’n, 518 S.W.3d 318, 328 (Tex. 2017). We therefore do not find the usage of “windstorm” in the Insurance and Property Code provisions instructive in elucidating the ordinary meaning of the term.

<details><summary>Other passages available</summary>

`cl4682256:5`

> [J-75A&B-2020] - 5 “functional approach” to the conception of intra-agency documents and adopted a “consultant corollary,” extending the exemption to communications between government agencies and outside consultants hired by them. Dep’t of Interior and Bureau o f Indian Affairs v. Klamath Water Users Protective Ass’n , 532 U.S. 1, 7-11, 121 S. Ct. 1060, 1065-67 (2001) (quoting 5 U.S.C. §552(b)(5)). These courts generally reason that, in “eliciting candid and honest advice from outside consultants,” it is “crucial” that the agency and the consultant can expect that their communications will remain confidential. Nat’l Inst. of Military Justice v. DOJ, 512 F.3d 677, 685 (D.C. Cir. 2008); see also id. at 683 (“[F]ederal agencies occasionally will encounter problems outside their ken, and it clearly is preferable that they enlist the help of outside experts skilled at unraveling their knotty complexities.”). Notably, to date, the Supreme Court of the United States has declined to address the propriety of this consultant corollary in FOIA jurisprudence. See Klamath, 532 U.S. at 12, 121 S. Ct. at 1067.
>
> The appeals officer also found that an attorney-client relationship existed between the Department and the McNees firm, and that DCED and Econsult were co-clients of that firm. See Finnerty, No. AP 2018 -0194, slip op. at 19; see also Finnerty, No. AP 2018-0247, slip op. at 15. For these reasons, he concluded that a portion of the withheld records were protected by the attorney-client privilege and the work-product doctrine. See id.
>
> The Authority filed petitions for review in the Commonwealth Court. Just before oral argument convened, the Department made an additional tender, asserting that it was disclosing all documents that had initially been withheld on the basis of the attorney-client and/or work-product privileges. DCED also sought a stipulation that as a result of the production, the issues were moot, but the Authority did not agree.
>
> [J-75A&B-2020] - 6

`cl6320573:8`

> 5 In addition to the exception at issue here, the TAIA contains several exclusions for certain types of agreements and provisions. See TEX. INS. CODE § 151.105.
>
> Here, the jury considering the Lees’ claims for personal injury found Maxim negligent and partially responsible for Lee’s harm. Under TAIA sections 151.102 and 151.104, therefore, any provision in the Equipment Lease or the Berkel CGL Policy that requires Berkel or Zurich to insure Maxim against claims caused by Maxim’s own negligence would be void. The parties agree that Zurich’s liability hinges on whether the TAIA’s employee exception applies to the Lees’ claims—that is, on whether Lee was “an employee of the indemnitor,” Berkel. Id. All parties agree that Lee—who worked for Skanska—is not Berkel’s “employee” under the common, ordinary meaning of that term. But Maxim contends that we should construe “employee” in section 151.103 to include any person or entity that the TWCA would treat as an employee of the indemnitor.
>
> “Statutory construction is a question of law for the court to decide.” Tex. Dep’t of Transp. v. Needham, 82 S.W.3d 314, 318 (Tex. 2002). “We review issues of statutory construction de novo.” Tex. Lottery Comm’n v. First State Bank of DeQueen, 325 S.W.3d 628, 635 (Tex. 2010). “When construing a statute, our primary objective is to determine the Legislature’s intent which, when possible, we discern from the plain meaning of the words chosen.” In re Estate of Nash, 220 S.W.3d 914, 917 (Tex. 2007); see also City of LaPorte v. Barfield, 898 S.W.2d 288, 292 (Tex. 1995) (“Legislative intent remains the polestar of statutory construction.”).

`cl11259842:3`

> “In contract law, the terms ‘ambiguous’ and ‘ambiguity’ have a more specific meaning than merely denoting a lack of clarity in language.” RSUI Indem. Co. v. Lynd Co. , 466 S.W.3d 113, 119 (Tex. 2015). If a written policy “is so worded that it can be given a definite or certain legal meaning, then it is not ambiguous.” Nat’l Union Fire Ins. , 907 S.W.2d at 520. But if the language “is subject to two or more reasonable interpretations, it is ambiguous.” Id .
>
> Should we conclude that the language is ambiguous, “we must resolve the uncertainty by adopting the construction that most favors the insured.” RSUI, 466 S.W.3d at 118. As the term at issue here appears in a limitation on coverage, “we must do so ‘even if the construction urged by the insurer appears to be more reasonable or a more accurate reflection of the parties’ intent.’” Id. (quoting Nat’l Union Fire Ins. Co. of Pittsburgh v. Hudson Energy Co., 811 S.W.2d 552, 555 (Tex. 1991)).
>
> III. Analysis
>
> With these principles in mind, we turn to the question of whether a tornado unambiguously qualifies as a windstorm for purposes of determining whether the applicable policy’s windstorm deductible applies. Insurer argues that “ windstorm” is not ambiguous given its plain meaning—a storm with strong and violent wind, which encompasses a tornado. By contrast, Insureds contend that “windstorm” is ambiguous because there is more than one reasonable ordinary meaning of the term, including one that excludes a tornado.

`cl11259842:6`

> Undoubtedly, some tornadoes occur amidst broader weather events that may not be classified as windstorms because of significant precipitation.8 However, the classification of the accompanying weather event in which a tornado forms has no bearing on whether the tornado itself is a windstorm. Rather, a tornado is merely one of multiple elements that may or may not be part of a particular weather event. A tornado is a windstorm in and of itself, and this is true regardless of whether it is a subset of a broader storm involving precipitation. Stated another way, a weather event may not qualify as a windstorm depending on the amount of precipitation involved, but that has no effect on the fact that, based on the ordinary meanings of the terms, a tornado is always a windstorm.
>
> 7 See Tornado, COLLINS ENGLISH DICTIONARY, https:// www.collinsdictionary.com/us/dictionary/english/tornado (last visited Feb. 12, 2026 ) (“a localized, violently destructive windstorm occurring over land, esp. in the M iddle West, and characterized by a long, funnel-shaped cloud extending toward the ground and made visible by condensation and debris”).
>
> 8 Insureds additionally assert that a windstorm references “a weather event with straight-line winds, also known as a ‘derecho ,’” which is distinct from the rotating winds that make up a tornado. No definitions of “windstorm” distinguish between rotating winds and straight-line winds. And notably, Merriam-Webster defines “derecho” as “ a large fast-moving complex of thunderstorms with powerful straight-line winds that cause widespread destruction.” Derecho, MERRIAM-W EBSTER, https://www.merriam-webster. com/dictionary/derecho (last visited Feb. 12, 2026). Despite a derecho’s express association with thunderstorms, which could certainly be considered events with precipitation, Insureds maintain that a derecho is a windstorm while insisting that a tornado, which is not defined in reference to any form of precipitation, is not.

</details>

| | Label | Reason |
|---|---|---|
| Rater A | `supported` | Step 1: cl11259842:7 says the provisions 'include broad enumerated terms with ordinary meanings that encompass accompanying narrower terms' and nothing suggests the lists exclude the narrower term. |
| Rater B | `supported` | cl11259842:7 says the Insurance and Property Code lists name tornadoes and windstorms separately but include broad terms encompassing narrower ones, so they do not show exclusion. |

**Recommended:** `supported` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] first_amendment_employee-cc-1 · citation_check · Ciarametaro v. City of Gloucester (ca1, 2023-11-28)

Source: [https://www.courtlistener.com/opinion/9447400/ciarametaro-v-city-of-gloucester/](https://www.courtlistener.com/opinion/9447400/ciarametaro-v-city-of-gloucester/) · opinion 9905225 · cited authority as it appears: `Camreta v. Greene, 563 U.S. 692, 709 n.7 (2011)`

**Claim:** Appellate courts have held that a public employee's judicial testimony was not protected under Pickering where it criticized third parties with whom the employer wanted to preserve a strong working relationship.

**Cited passage:** `cl9905225:10`

> In a supplemental letter to the court, Ciarametaro points to Swartzwelder v. McNeilly, 297 F.3d 228 (3d Cir. 2002). But Swartzwelder is plainly distinguishable on its facts. That case involved a sweeping police department policy that required "the vast rank and file" of officers to obtain approval before giving expert opinion testimony. 297 F.3d at 231–32, 237 (quoting United States v. Nat'l Treasury Emp. Union, 513 U.S. 454, 472 (1995)). The breadth of that prior restraint invited a "tailoring requirement," id. at 236, which the police department's broad policy could not satisfy, id. at 241. By contrast, this case involves a town responding to specific testimony by a specific official. Hence, it does not present the overbreadth defect that took center stage in Swartzwelder.
>
> In the same letter, Ciarametaro also cites to Brady v. Tamburini, 518 F. Supp. 3d 570 (D.R.I. 2021). Brady is a district court case, and district court decisions "do not necessarily settle constitutional standards or prevent repeated claims of qualified immunity." Camreta v. Greene, 563 U.S. 692, 709 n.7 (2011). In any event, Brady is inapposite. There, a police department disciplined a detective for comments he made to a newspaper reporter. 518 F. Supp. 3d at 577. The district court concluded that Pickering balancing favored the officer, because the department "presented no evidence" that the officer's speech actually or potentially disrupted department operations. Id. at 586. That is not the case here, where the City Officials had ample reason to believe that Ciarametaro's speech threatened relationships with commercial fishermen.

<details><summary>Other passages available</summary>

`cl9905225:5`

> Qualified immunity shields public officials from personal liability for "actions taken while performing discretionary functions." Lynch v. City of Boston, 180 F.3d 1, 13 (1st Cir. 1999). The goal of qualified immunity is to "give[] government officials breathing room to make reasonable but mistaken judgments about open legal questions." Ashcroft v. al-Kidd, 563 U.S. 731, 743 (2011). To achieve that goal, a court will grant qualified immunity unless it is "sufficiently clear 'that every reasonable official would [have understood] that what he [was] doing violate[d]'" the plaintiff's rights. Reichle v. Howards, 566 U.S. 658, 664 (2012) (first alteration in the original) (quoting Ashcroft, 563 U.S. at 741). Qualified immunity therefore protects "all but the plainly incompetent or those who knowingly violate the law." Malley v. Briggs, 475 U.S. 335, 341 (1986).
>
> To surmount qualified immunity, a plaintiff must show that 1) the official "violated a statutory or constitutional right," and 2) the ostensibly violated right was "clearly established" at the time of the challenged conduct. Ashcroft, 563 U.S. at 735. The plaintiff must point to controlling authority, or a "robust consensus" of persuasive authority, clearly demonstrating the "violative nature of [the defendant's] particular conduct." Id. at 741–42 (internal citations and quotations omitted). That authority need not be "directly on point," but a plaintiff also may not "define clearly established law at a high level of generality." Id. at 741–42. Instead, the plaintiff must identify authority that is sufficiently analogous to "place[] the statutory or constitutional question beyond debate." Id. at 741.
>
> B.
>
> To determine whether a public employer violates an employee's First Amendment rights by retaliating against him on account of his speech, we employ a three-step standard. See Davignon v. Hodgson, 524 F.3d 91, 100 (1st Cir. 2008).

`cl11107767:12`

> We begin with the lodestar question of whether there is a genuine dispute as to whether either category of Burch’s speech is protected. We answer this by assessing whether a reasonable factfinder could find that Burch established the first two Pickering steps: (1) that he “spoke on a matter of public concern,” and (2) that he “spoke as a private citizen” rather than as “a public employee.” Dodge, 56 F.4th at 777 (quoting Johnson, 658 F.3d at 961). The first step poses a question of law. Greisen, 925 F.3d at 1109. The second poses a mixed question of law and fact. Posey, 546 F.3d at 1126–29.
>
> a
>
> The first step—assessing whether Burch’s speech addressed a matter of public concern—presents a low bar. “Speech involves a matter of public concern when it can fairly be considered to relate to ‘any matter of political, social, or other concern to the community.’” Eng, 552 F.3d at 1070 (quoting Johnson v. Multnomah County, 48 F.3d 420, 422 (9th Cir. 1995)). “It is only ‘when it is clear . . . the information would be of no relevance to the public’s evaluation of the performance of governmental agencies’” that such speech does not address a matter of public concern. Ulrich v. City & County of San Francisco, 308 F.3d 968, 978 (9th Cir. 2002) (alteration in original) (quoting Pool v. Vanrheen, 297 F.3d 899, 907 (9th Cir. 2002)).
>
> As a matter of law, Burch’s yard sign expressing his political support for England’s mayoral opponent addresses a matter of public concern. See Dodge, 56 F.4th at 773, 777 (holding that public employee wearing a “Make America Great Again” hat to workplace training addressed a matter of public concern because expressions regarding candidates for office “inherently relate to the political, social, or other concern to the community” (internal quotation marks and citation omitted)).

`cl11110987:8`

> If the employee satisfies those requirements, then the First Amendment is implicated, but more is required to establish that the Amendment protects the public employee’s speech. The court must also assess whether the government employer “had an adequate justification for treating the employee differently from any other member of the public based on the government’s needs as an employer.” Lane v. Franks, 573 U.S. 228, 242 (2014) (internal quotation marks omitted). That assessment requires the court to “balance . . . the interests of the [employee], as a citizen, in commenting upon matters of public concern and the interest of the State, as an employer, in promoting the efficiency of the public services it performs through its employees.” Pickering v. Bd. of Educ., 391 U.S. 563, 568 (1968). If the balance tips in the employee’s favor, the First Amendment will protect the public employee’s speech.
>
> In this case, the district court addressed only whether Long spoke as a citizen, concluding that her claim failed at the threshold. Accordingly, we focus only on that question.
>
> For a public employee to demonstrate that she spoke as a citizen, she must establish that her speech fell “outside of [her] official responsibilities.” Shara v. Maine-Endwell Cent. Sch. Dist., 46 F.4th 77, 83 (2d Cir. 2022). To determine whether a public employee has met that burden, a court must “examine the nature of the plaintiff’s job responsibilities, the nature of the speech, and the relationship between the two, along with other contextual factors such as whether the plaintiff’s speech was also conveyed to the public.” Id. (internal quotation marks omitted). “[S]peech may be pursuant to an employee’s official duties when it is part-and-parcel of the employee’s concerns about [her] ability to properly execute [her] duties.” Id. (internal quotation marks omitted). Ultimately, whether a public employee’s speech was “pursuant to” her job duties is a “practical” inquiry, and a court should not “constru[e] a government employee’s official duties too narrowly” by relying solely on a formal job description. Weintraub v. Bd. of Educ., 593 F.3d 196, 202 (2d Cir. 2010) (internal quotation marks omitted).

`cl9905225:11`

> Our own review also reveals no case clearly establishing that Ciarametaro's speech was categorically entitled to First Amendment protection. See Elder v. Holloway, 510 U.S. 510, 512 (1994) ("[A]ppellate review of qualified immunity dispositions is to be conducted in light of all relevant precedents . . . ."). In fact, several appellate cases have held that a public employee's judicial testimony was not protected under Pickering when the testimony criticized third parties with whom the public employer wished to maintain a strong working relationship. See, e.g., Worrell v. Henry, 219 F.3d 1197, 1208 (10th Cir. 2000) (district attorney could withdraw an offer of employment to serve as the coordinator of a drug task force, because the offeree's past testimony on behalf of a criminal defendant risked relationships with a cooperating agency); Tedder v. Norman, 167 F.3d 1213, 1215 (8th Cir. 1999) (director of a law enforcement training center could demote his deputy, because the deputy's prior testimony in an excessive force case threatened relationships between the training center and the law enforcement agencies it trained); cf. Gilchrist v. Citty, 173 Fed. App'x 675, 685 (10th Cir. 2006) (forensic lab could demote an analyst who previously gave faulty testimony because, among other things, further testimony could threaten the lab's credibility in court).
>
> To be clear, we need not (and therefore do not) decide whether the value of Ciarametaro's speech outweighed the City Officials' interests under Pickering balancing. We hold only that the City Officials could have reasonably concluded that it did not. And even if the City Officials' reasoning was "mistaken, it would not have been egregiously so . . . . [A]ccordingly, qualified immunity is available." See Wagner v. City of Holyoke, 404 F.3d 504, 509 (1st Cir. 2005).
>
> IV.
>
> For the foregoing reasons, the judgment of the district court is affirmed.

</details>

| | Label | Reason |
|---|---|---|
| Rater A | `right_doc_wrong_passage` | Step 2: cl9905225:11 says 'several appellate cases have held that a public employee's judicial testimony was not protected under Pickering when the testimony criticized third parties with whom the public employer wished to maintain a strong working relationship'; cited cl9905225:10 distinguishes Swartzwelder and Brady. |
| Rater B | `right_doc_wrong_passage` | cited cl9905225:10 distinguishes Swartzwelder and Brady; same-opinion cl9905225:11 says several appellate cases held judicial testimony not protected under Pickering when it criticized third parties with whom the employer wished to maintain a strong relationship. |

**Recommended:** `right_doc_wrong_passage` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] insurance_duty_defend-cc-4 · citation_check · A.R. Wilfley & Sons, Inc. v. National Union Fire Insurance Company of Pittsburgh, PA; Federal Insurance Company; and United States Fire Insurance Company. (colo, 2026-09-21)

Source: [https://www.courtlistener.com/opinion/10984928/ar-wilfley-sons-inc-v-national-union-fire-insurance-company-of/](https://www.courtlistener.com/opinion/10984928/ar-wilfley-sons-inc-v-national-union-fire-insurance-company-of/) · opinion 11452592 · cited authority as it appears: `In re Phillips, 139 P.3d 639, 643`

**Claim:** An insurer acts in bad faith if its breach of the duty to defend was unreasonable, frivolous or unfounded, and an insurer unsure of its duty may defend under a reservation of rights while seeking a declaratory judgment.

**Cited passage:** `cl11452592:8`

> ¶27 Before surveying the coverage tower, we pause to address several issues that form the foundation of our analysis: the source of our jurisdiction, the standard of review, and the principles governing contract interpretation. With this bedrock laid down, we briefly digress to explain the differences between umbrella coverage and excess coverage. Our focus then shifts to Federal's coverage, and we proceed to give effect to the unambiguous policy language, informed where appropriate by decisions from other jurisdictions. We ultimately conclude that an umbrella/excess insurer does not become the primary insurer's stopgap—or inherit its obligations—simply because the primary insurer becomes insolvent. Therefore, an occurrence covered by Reliance's scheduled underlying policies remains covered even though Reliance has become insolvent. And because, as pertinent here, the Federal Policies can be triggered only by occurrences that are
>
> "not covered" by Reliance's policies or when the underlying limits have been exhausted, we answer the certified question in the negative.
>
> A. The Analytical Groundwork: Jurisdiction, Standard of Review, and Contract-Interpretation Principles
>
> ¶28 First, our jurisdiction. C.A.R. 21.1(a) allows us to answer questions of Colorado law certified by a federal court that "may be determinative of the cause then pending in the certifying court" and for which there is "no controlling precedent" from our court. Hamilton v. Amazon.com Servs. LLC, 2024 CO 60, ¶ 21, 555 P.3d 620, 625-26 (citing In re Phillips, 139 P.3d 639, 643 (Colo. 2006)). Whether to accept a certified question lies within our sound discretion. Id., 555 P.3d at 626. We accepted jurisdiction here because the certified question presents an issue on which we have not yet spoken, and our answer will determine whether Wilfley may tap the excess-coverage portion of the Federal Policies.

<details><summary>Other passages available</summary>

`cl11452592:14`

> ¶49 Because an "insurance policy is merely a contract that courts . . . interpret in line with well-settled principles of contract interpretation," it is our task to ascertain and give effect to the parties' intent by reading the policy as a whole and harmonizing its provisions so none will be rendered meaningless. Cyprus Amax Mins. Co., 74 P.3d at 299, 307; see also Pub. Serv. Co. of Colo. v. Wallis &Cos., 986 P.2d 924, 933 (Colo. 1999) (applying principles of contract interpretation to give effect to the parties' chosen language and to avoid rendering a term superfluous); Rocky Mountain Prestress, LLC v. Liberty Mut. Fire Ins. Co., 960 F.3d 1255, 1262 (10th Cir. 2020) (applying Colorado law to give effect to the term "defective workmanship" in an insurance policy while avoiding an interpretation that would strip the phrase of its meaning). Here, the parties intended for the Federal Policies to trigger first-
>
> dollar obligations only when an occurrence is not covered by a scheduled underlying policy—i.e., only when an occurrence falls outside the scope of coverage afforded by a scheduled underlying policy. And nothing in the Federal Policies indicates that the parties intended insolvency to transform a covered occurrence into an uncovered one.

`cl4532507:15`

> “An insurer acts in bad faith if its breach of the duty to defend was unreasonable, frivolous, or unfounded.” Am. Best Food, 168 Wn.2d at 412. When an insurer is unsure as to whether the duty to defend applies, “it may defend under a reservation of rights while seeking a declaratory judgment that it has no duty to defend.” Truck Ins. Exch. 147 Wn.2d at 761. This reservation of rights means that the insurer “avoids breaching its duty to defend while seeking to avoid waiver and Because we find that the exception does not apply, we do not reach the issue of whether a Treaty is “disclosed by public record.” Robbins v. Mason County Title Ins., No. 96726-1 estoppel” while giving the insured the benefit of the doubt. Id. When an insurer wrongfully refuses to defend, there is a rebuttable presumption of harm to the insured. Am. Best Food, 168 Wn.2d at 411-12 (citing Kirk v. Mt. Airy Ins. Co., 134 Wn.2d 558, 563, 951 P.2d 1124 (1998)). When an insurer breaches in bad faith, it is estopped from denying coverage. Kirk, 134 Wn.2d at 564.
>
> In American Best Food, we held that the insurer acted in bad faith as a matter of law when it declined to defend based on its own interpretation of the law. 168 Wn.2d at 411. In that case, a nightclub patron sued American Best Food’s nightclub for negligence when employees “dump[ed] him on the sidewalk” after he had been shot by another patron. Id. at 403. The insurer, Alea, refused to defend because the insurance policy included an exception for injuries arising from assault and battery. Id. At the time of the case, Washington case law indicated that preassault negligence was included in an assault and battery exclusion because the cause of action still arose from the actual assault. Id. at 406-07 (citing McAllister v. Agora Syndicate, Inc., 103 Wn. App. 106, 11 P.3d 859 (2000)). Alea relied on this case law to deny coverage.

`cl9226166:11`

> a subrogation action against the tenant under the facts of this case.” Id. ¶ 39 We agree with Presiding Justice McDade’s dissent and find Dix is not applicable to this case. Dix is a subrogation case, which is governed by equitable principles. To “subrogate” means “[t]o substitute (a person) for another regarding a legal right or claim.” Black’s Law Dictionary 1726 (11th ed. 2019). When put into context, subrogation is defined as “[t]he principle under which an insurer that has paid a loss under an insurance policy is entitled to all the rights and remedies belonging to the insured against a third party with respect to any loss covered by the policy.” Id. The issue in this case does not involve the equitable principles of subrogation. While the underlying claim in Tazewell County case No. 17-L-49 was a subrogation action filed by Auto-Owners in McIntosh’s name against Workman to recoup payment for the fire damage to the premises, the underlying claim in Tazewell County case No. 17-L-49 against the Shecklers was a third-party contribution claim brought by Workman. Thus, this court’s holding in Dix is not relevant here where the issue is not one of subrogation but whether Auto-Owners owes a duty to defend or indemnify the Shecklers against Workman’s third-party contribution claim. ¶ 40 Moreover, Dix is not applicable to this case, where this court in Dix expressly limited its holding to “the particular facts of [that] case.” 149 Ill. 2d at 323. ¶ 41 Having found Dix is not applicable, we look to the insurance policy to determine whether the Shecklers are coinsured for purposes of Auto-Owners’ duty to defend or indemnify under the policy. “A court’s primary objective in construing the language of an insurance policy is to ascertain and give effect to the intentions of the parties as expressed by the language of the policy.” Valley Forge Insurance Co., 223 Ill. 2d at 362. “If the words used in the policy, given their plain and ordinary meaning, are unambiguous, they must be applied as written.” Id. at 363. ¶ 42 When looking at the plain language

`cl9226166:8`

> duty to defend. See Hacker, 388 Ill. App. 3d at 391 (“The Dix court’s analysis of the equities of subrogation is not relevant in determining an insurance company’s duty to defend.”). ¶ 28 A. Standard of Review ¶ 29 “When the parties file cross-motions for summary judgment, they agree that only questions of law are involved and invite the court to decide the issues based on the record.” State Farm Mutual Automobile Insurance Co. v. Elmore, 2020 IL 125441, ¶ 19 (citing Bremer v. City of Rockford, 2016 IL 119889, ¶ 20). We review summary judgment orders de novo. Id. ¶ 30 B. Duty to Defend or Indemnify ¶ 31 The issue presented in this matter is whether Auto-Owners owes a duty to defend or indemnify the Shecklers against a third-party contribution claim. “To determine whether an insurer has a duty to defend its insured from a lawsuit, a court must compare the facts alleged in the underlying complaint to the relevant provisions of the insurance policy.” Valley Forge Insurance Co., 223 Ill. 2d at 363. “The duty to indemnify arises only when the insured becomes legally obligated to pay damages in the underlying action that gives rise to a claim under the policy.” Zurich Insurance Co., 118 Ill. 2d at 52. ¶ 32 Before we can determine whether Auto-Owners owes a duty to defend or indemnify the Shecklers against a third-party contribution claim, we must first determine whether the Shecklers were coinsured under the insurance policy. For purposes of this analysis, we view the insurance policy at issue to be one policy that includes multiple types of coverages. ¶ 33 Auto-Owners argues that, when looking at the plain language of the insurance policy, the Shecklers were not coinsureds where the policy only named McIntosh and his wife as covered insureds. The Shecklers acknowledge they were not named as covered insureds under the insurance policy. However, the Shecklers argue that, under an equitable extension of Dix, they are considered additional insureds as a matter of law under the lease provisions and the insurance policy. Thus, we review this court’s analysis

</details>

| | Label | Reason |
|---|---|---|
| Rater A | `wrong_document` | Step 3: the cited cl11452592:8 concerns jurisdiction over certified questions, the standard of review and contract-interpretation principles; the bad-faith and reservation-of-rights statement is in cl4532507:15, a different opinion. |
| Rater B | `wrong_document` | Cited cl11452592:8 is Colorado coverage roadmap; cl4532507:15 (different opinion) states bad faith if breach unreasonable, frivolous or unfounded and defending under reservation of rights while seeking declaratory judgment. |

**Recommended:** `wrong_document` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] limitations_discovery_rule-qa-3 · qa_citation · Sec. Bank & Trust Co. v. Larkin, Hoffman, Daly & Lindgren, Ltd. (minn, 2018-06-27)

Source: [https://www.courtlistener.com/opinion/8284769/sec-bank-trust-co-v-larkin-hoffman-daly-lindgren-ltd/](https://www.courtlistener.com/opinion/8284769/sec-bank-trust-co-v-larkin-hoffman-daly-lindgren-ltd/) · opinion 8250811 · cited authority as it appears: `Frederick v. Wallerich , 907 N.W.2d 167, 173`

**Question:** In Security Bank & Trust v. Larkin, Hoffman, how did the Minnesota Supreme Court define accrual of a cause of action, and what elements must a plaintiff plead for transactional legal malpractice?

**Reference notes:** Must mention: accrual is the point at which a plaintiff can allege facts sufficient to survive a motion to dismiss and requires operative facts supporting each element; a cause of action does not exist as a matter of law until it accrues; the four elements are an attorney-client relationship, negligent acts or breach, proximate cause of damages, and that but for the conduct the plaintiff would have obtained a more favorable result.

**Chunks either rater chose:**

`cl8250811:4`

> The parties' arguments contemplate two potential routes for Security Bank to have standing as personal representative: as successor to a cause of action that accrued to Savoie during his lifetime, or in its own right regardless of whether a cause of action accrued before or after Savoie's death. As set out below, neither route leads to standing for Security Bank.
>
> "Accrual" refers to the point in time when "a plaintiff can allege sufficient facts to survive a motion to dismiss for failure to state a claim upon which relief can be granted." Frederick v. Wallerich , 907 N.W.2d 167, 173 (Minn. 2018) (citing Antone , 720 N.W.2d at 335 ). Accrual of a cause of action requires the existence of operative facts supporting each element of the claim. See id. ("An analysis of when a claim accrues ... necessarily involves consideration of all elements of the claim."); Cause of Action , Black's Law Dictionary (10th ed. 2014) (defining "cause of action" as "[a] group of operative facts giving rise to one or more bases for suing; a factual situation that entitles one person to obtain a remedy in court from another person"). Thus, a cause of action does not "exist" as a matter of law until it accrues-the point at which the operative facts supporting each element of the claim come into existence.
>
> To state a claim for legal malpractice related to transactional legal services, which are at issue here, a plaintiff must plead four elements: (1) the existence of an attorney-client relationship; (2) acts constituting negligence or breach of contract; (3) that such acts were the proximate cause of plaintiff's damages; and (4) that, but for the attorney's conduct, the plaintiff would have obtained a more favorable result in the relevant matter. Frederick , 907 N.W.2d at 173.
>
> The parties do not dispute that the facts alleged in Security Bank's complaint satisfy the elements of a claim for legal malpractice insofar as Security Bank stands in its capacity as personal representative.1

Candidate window: `cl8250811:2`, `cl8250811:3`, `cl8250811:4`, `cl8250811:5`, `cl8250811:6`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl8250811:4']` | cl8250811:4 gives the accrual definition, the operative-facts-per-element requirement, the non-existence-before-accrual point and the four elements. |
| Rater B | `['cl8250811:4']` | Chunk 4 defines accrual (facts sufficient to survive motion to dismiss, operative facts for each element, claim does not exist until it accrues) and lists the four malpractice elements. |

**Recommended:** `['cl8250811:4']` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] miranda_custody-cc-1 · citation_check · People v. Robinson (ny, 2025-10-23)

Source: [https://www.courtlistener.com/opinion/10717764/people-v-robinson/](https://www.courtlistener.com/opinion/10717764/people-v-robinson/) · opinion 11176209 · cited authority as it appears: `New York v Quarles, 467 US 649 [1984]`

**Claim:** A statement of frustration like 'I ain't got nothin' to say' does not revoke a Miranda waiver, because a request to stop questioning after waiver must be unambiguous and unequivocal.

**Cited passage:** `cl11176209:6`

> Huffman does not support a different rule. There, the defendant and a number of other individuals were gathered behind a deli in the middle of the night when police officers approached, causing them to scatter. The officers found the defendant hiding in a bush, drew their weapons, and asked "What are you doing back here?," to which the defendant replied "We were trying to break into that store" (see Huffman, 41 NY2d at 30). In holding that the officer's question did not constitute interrogation, we emphasized that the statement was made not only at the scene but at a particularly volatile moment (see id. at 34 [describing the situation confronting the officers as "a potential assault from an unknown person fleeing from what appeared to be the scene of criminal activity" and noting that "immediate clarification was necessary before taking drastic action"]). In the almost half-century since Huffman was decided, the United States Supreme Court has made clear that the existence of interrogation turns on the foreseeability of an incriminating response (see Innis, 446 US at 301-302). The volatile circumstances we referenced in Huffman are more relevant, instead, to a public safety exception to the Miranda rule (see New York v Quarles, 467 US 649 [1984]). Huffman must be read with these jurisprudential developments in mind, but at no point has it ever supported a rule that questions asked at the scene of a suspected crime, during or shortly after the suspected crime's commission, are categorically exempt from Miranda.
>
> Notwithstanding this constitutional error, the Appellate Division correctly concluded that the admission of defendant's unwarned statement was harmless beyond a reasonable doubt. The evidence at trial, including the victim's and Officer Sasso's unrebutted trial testimony and the video footage, overwhelmingly established defendant's guilt. Further, there is no reasonable possibility that the admission of defendant's statement affected the outcome of the trial (see People v Best, 19 NY3d 739, 744 [2012]; People v Crimmins, 36 NY2d 230, 240-241 [1975]).
>
> Accordingly, the order of the Appellate Division should be affirmed.

<details><summary>Other passages available</summary>

`cl6105386:11`

> The same is true of DeChoudens's testimony that Doe spoke in 1985 with a Dominican accent, especially because the 795-SSA form -- which, as we have explained, Doe has not shown was improperly admitted into evidence -- itself contained an admission by Doe that he spoke with a Dominican accent in 2014, and that Rincon testified at trial that she recalled Doe at that time spoke "more like a Dominican . . . than a Puerto Rican" and that she "could tell he was acting as a Puerto Rican" because "[h]e was using a lot of expressions that are very stereotypical, and . . . just didn't come out right." See Ahern v. Scholz, 85 F.3d 774, 786 (1st Cir. 1996) (noting that an error does not "rise[] to the level of harmful error if . . . 'the evidence omitted was cumulative as to other admitted evidence'" (quoting Doty v. Sewall, 908 F.2d 1053, 1057 (1st Cir. 1990))). We thus reject Doe's Miranda-based challenge to his convictions on harmless error grounds, without thereby suggesting that the interview DeChoudens conducted constituted a custodial interrogation.
>
> IV.
>
> For the aforementioned reasons, we affirm.

`cl11176209:5`

> Contrary to the lower courts' reasoning, it is not dispositive that defendant was questioned in the immediate aftermath of the altercation, while the officers were still determining whether a crime had occurred—circumstances Supreme Court seemingly relied on in deeming the encounter a "classic case of investigatory questioning" that did not require Miranda warnings. Our case law draws no categorical distinction between interrogation and so-called investigatory questioning. Interrogation is almost definitionally investigatory in nature. And while we have recognized a "distinction between coercive interrogation and permissible street inquiry" (Huffman, 41 NY2d at 32), the most salient difference between these categories is not when the questioning takes place, but the presence or absence of custody (see id. at 32-33, distinguishing between People v Rodney P. [Anonymous], 21 NY2d 1 [1967], and People v Shivers, 21 NY2d 118 [1967]). As we have explained, "routine police investigation of suspicious conduct on the street generally does not entail a significant deprivation of freedom which would require Miranda warnings" (Matter of Kwok T., 43 NY2d 213, 218 [1977]). Absent "both the elements of police 'custody' and police 'interrogation,' " there is no "constitutional requirement that the police recite interrogation warnings when they direct questions or comments at members of the public or solicit information and assistance" (see Huffman, 41 NY2d at 33 [emphasis added]). But where, as here, investigatory questions are directed to a person who is in custody, under circumstances police should know are likely to yield an incriminating response, Miranda warnings are required.

`cl11176209:4`

> The decisions of the lower courts in this case predate the guidance we provided in Cabrera. Here, the record similarly lacks support for Supreme Court's conclusion that defendant was not in custody when he was handcuffed, surrounded by numerous officers, and questioned about the altercation. Defendant remained restrained as he was searched, questioned, and repeatedly accused of theft and assault by the victim over an approximately eight-minute period. Defendant's freedom of movement was restricted to a degree comparable to a formal arrest, and he was given no reason to believe he would shortly be released or permitted to leave. Indeed, a reasonable person in defendant's position would likely have understood that he was suspected of committing a crime, and "that removal or maintenance of the handcuffs depended on . . . [him] responding to questions posed"—a coercive circumstance federal courts have treated as indicative of custody in factually similar cases (see United States v Newton, 369 F3d 659, 677 [2d Cir 2004]).
>
> The next question is whether defendant was subjected to interrogation. Under well settled law, interrogation "refers not only to express questioning, but also to any words or actions on the part of the police (other than those normally attendant to arrest and custody) that the police should know are reasonably likely to elicit an incriminating response from the suspect" (Rhode Island v Innis, 446 US 291, 301 [1980]; People v Ferro, 63 NY2d 316, 322 [1984]). In this case, defendant was asked several express questions about his physical altercation with the victim. Over the course of the encounter, the officers also made defendant aware they had witnessed him punch the victim and heard the victim's version of events. And they continued asking defendant for his side of the story even after Officer Sasso observed that he was "not talking." In these circumstances, it was foreseeable that the officers' words and actions would generate an incriminating response (see Innis, 446 US at 302).

`cl5124709:8`

> Switching gears, Wesson claims that he attempted to withdraw his Miranda waiver when, during his interrogation, he told police officers “I ain’t got nothin’ to say to y’all.” R.36 at 51–52. But a request to end an interrogation after a Miranda waiver must be unambiguous and unequivocal. Berghuis, 560 U.S. at 381; see Davis v. United States, 512 U.S. 452, 461–62 (1994). Wesson’s statement was neither. As we have said before in handling a Miranda-waiver-revocation claim, “context matters.” Bird v. Brigano, 295 F. App’x 36, 38 (6th Cir. 2008). When viewed in the light shed by his immediately preceding statements, Wesson’s statement that he “ain’t got nothin’ to say to y’all” more accurately conveys an expression of frustration at his plight, a murder suspect faced with an eyewitness victim and a murder weapon connecting him to the deed, than an effort to end the interview. Confirming the point, we have rejected similar claims with equivocal requests to end an interrogation. United States v. Hurst, 228 F.3d 751, 760 (6th Cir. 2000) (holding defendant’s “refusal to answer a question about stolen firearms” was not an unequivocal invocation where he said at the beginning of the interview that “he was willing to answer only specific questions”); cf. Franklin v. Bradshaw, 545 F.3d 409, 415 (6th Cir. 2008) (finding no unreasonable application of law in state court holding defendant’s single statement that he did not want to tell his side of the story was not an unequivocal or unambiguous invocation of his rights in light of his answers to other police questions).
>
> We affirm.

</details>

| | Label | Reason |
|---|---|---|
| Rater A | `wrong_document` | Step 3: cl5124709:8 (Wesson, different opinion) says a post-waiver request to end an interrogation must be unambiguous and unequivocal and that the statement 'ain't got nothin' to say' conveyed frustration; cited cl11176209:6 (Robinson) discusses Huffman and the public safety exception. |
| Rater B | `wrong_document` | cited cl11176209:6 is about Huffman and harmlessness; cl5124709:8 (a different opinion) says a post-waiver request to end questioning must be unambiguous and unequivocal and "I ain't got nothin' to say" expressed frustration. |

**Recommended:** `wrong_document` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] miranda_custody-qa-1 · qa_citation · People v. Robinson (ny, 2025-10-23)

Source: [https://www.courtlistener.com/opinion/10717764/people-v-robinson/](https://www.courtlistener.com/opinion/10717764/people-v-robinson/) · opinion 11176209 · cited authority as it appears: `Rhode Island v Innis, 446 US 291, 301 [1980]`

**Question:** In People v. Robinson, how did the New York Court of Appeals apply the custody and interrogation tests to a handcuffed man questioned by several officers at the scene of a fight?

**Reference notes:** Must mention: handcuffed, surrounded and questioned for about eight minutes with no reason to expect release, his freedom was restricted to a degree comparable to formal arrest, so he was in custody; interrogation covers words or actions police should know are reasonably likely to elicit an incriminating response, which the officers' questions and statements were.

**Chunks either rater chose:**

`cl11176209:4`

> The decisions of the lower courts in this case predate the guidance we provided in Cabrera. Here, the record similarly lacks support for Supreme Court's conclusion that defendant was not in custody when he was handcuffed, surrounded by numerous officers, and questioned about the altercation. Defendant remained restrained as he was searched, questioned, and repeatedly accused of theft and assault by the victim over an approximately eight-minute period. Defendant's freedom of movement was restricted to a degree comparable to a formal arrest, and he was given no reason to believe he would shortly be released or permitted to leave. Indeed, a reasonable person in defendant's position would likely have understood that he was suspected of committing a crime, and "that removal or maintenance of the handcuffs depended on . . . [him] responding to questions posed"—a coercive circumstance federal courts have treated as indicative of custody in factually similar cases (see United States v Newton, 369 F3d 659, 677 [2d Cir 2004]).
>
> The next question is whether defendant was subjected to interrogation. Under well settled law, interrogation "refers not only to express questioning, but also to any words or actions on the part of the police (other than those normally attendant to arrest and custody) that the police should know are reasonably likely to elicit an incriminating response from the suspect" (Rhode Island v Innis, 446 US 291, 301 [1980]; People v Ferro, 63 NY2d 316, 322 [1984]). In this case, defendant was asked several express questions about his physical altercation with the victim. Over the course of the encounter, the officers also made defendant aware they had witnessed him punch the victim and heard the victim's version of events. And they continued asking defendant for his side of the story even after Officer Sasso observed that he was "not talking." In these circumstances, it was foreseeable that the officers' words and actions would generate an incriminating response (see Innis, 446 US at 302).

Candidate window: `cl11176209:2`, `cl11176209:3`, `cl11176209:4`, `cl11176209:5`, `cl11176209:6`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl11176209:4']` | cl11176209:4 states the custody finding (handcuffs, officers, eight minutes) and the Innis interrogation test applied to the questions. |
| Rater B | `['cl11176209:4']` | cl11176209:4 applies custody (handcuffed, surrounded, about eight minutes, no reason to expect release) and interrogation (words/actions likely to elicit an incriminating response). |

**Recommended:** `['cl11176209:4']` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] miranda_custody-qa-2 · qa_citation · Hersie Wesson v. Tim Shoop (ca6, 2021-11-09)

Source: [https://www.courtlistener.com/opinion/5296147/hersie-wesson-v-tim-shoop/](https://www.courtlistener.com/opinion/5296147/hersie-wesson-v-tim-shoop/) · opinion 5124709 · cited authority as it appears: `United States v. Mahan, 190 F.3d 416, 422 (6th Cir. 1999)`

**Question:** Under the Sixth Circuit's decision in Wesson v. Shoop, what must be shown to establish that a Miranda waiver was involuntary, and what considerations does the coercion inquiry look to?

**Reference notes:** Must mention: some element of official coercion is a prerequisite; a waiver is coerced if the police activity was objectively coercive, sufficient to overbear the will, and the crucial motivating factor; considerations include the suspect's characteristics, whether warnings were given, length of questioning and deprivations.

**Chunks either rater chose:**

`cl5124709:3`

> In requiring a waiver to be voluntary, the Fifth Amendment does not concern itself “with moral and psychological pressures to confess emanating from sources other than official coercion,” say a fervid conscience, for the “privilege has always depended on the absence of police overreaching, not on ‘free choice’ in any broader sense of the word.” Colorado v. Connelly, 479 U.S. 157, 170 (1986) (quotation omitted). A prerequisite to finding that a defendant involuntarily waived his Miranda rights is some element of official coercion. A waiver is coerced if “(i) the police activity was objectively coercive; (ii) the coercion in question was sufficient to overbear the defendant’s will; and (iii) the alleged police misconduct was the crucial motivating factor in the defendant’s decision to offer the statement.” United States v. Mahan, 190 F.3d 416, 422 (6th Cir. 1999). The coercion inquiry looks to several potential considerations: the age, education, and other characteristics of the suspect; whether the No. 20-3613 Wesson v. Shoop Page 4 suspect was advised of his Miranda rights; the length of the questioning; and the use of physical punishment or the deprivation of food, sleep, or other creature comforts. See Schneckloth v. Bustamonte, 412 U.S. 218, 226 (1973) (consent to search).

Candidate window: `cl5124709:1`, `cl5124709:2`, `cl5124709:3`, `cl5124709:4`, `cl5124709:5`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl5124709:3']` | cl5124709:3 requires official coercion, gives the three-part test and lists the coercion considerations. |
| Rater B | `['cl5124709:3']` | cl5124709:3 says official coercion is a prerequisite, gives the three-part coercion test, and lists suspect characteristics, warnings, length of questioning and deprivations. |

**Recommended:** `['cl5124709:3']` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] negligence_duty-cc-5 · citation_check · Snay v. Burr (Slip Opinion) (ohio, 2021-11-24)

Source: [https://www.courtlistener.com/opinion/5300575/snay-v-burr-slip-opinion/](https://www.courtlistener.com/opinion/5300575/snay-v-burr-slip-opinion/) · opinion 5129137 · cited authority as it appears: `Ramby v. Ping, 2d Dist. Greene No. 93-CA-52, 1994 WL 124829 (Apr. 13, 1994)`

**Claim:** The Ohio Supreme Court cited with approval a decision declining to impose a duty to remove off-road hazards that make only off-road travel unsafe, reasoning that otherwise every roadside tree or fixed object would create potential liability.

**Cited passage:** `cl5129137:13`

> {¶ 25} Recognizing that “a motorist is not free to drive on the right-of-way as he or she pleases,” Turner, 118 Ohio St.3d 215, 2008-Ohio-2010, 887 N.E.2d 1158, at ¶ 17, we reasoned that the off-road utility pole did not interfere with the public’s use of the road, because “a motorist properly using the usual and ordinary course of travel would not come into contact with” it, id. at ¶ 26. In reaching this decision, we cited with approval Ramby v. Ping, 2d Dist. Greene No. 93-CA-52, 1994 WL 124829 (Apr. 13, 1994), in which the Second District Court of Appeals “declined to extend Manufacturer’s to impose a duty on adjacent landowners and municipalities to keep a right-of-way free of objects that pose a danger to vehicles
>
> SUPREME COURT OF OHIO that may foreseeably leave the traveled portion of the roadway.” Turner at ¶ 23. We also quoted the Second District’s rationale:
>
> “No precedent exists for imposing a duty on public or private
>
> landowners to remove an off-road hazard that renders only off-road
>
> travel unsafe, unless the off-road travel is shown to be an aspect of
>
> the usual and ordinary course of travel on the roadway. Otherwise,
>
> every tree and solid fixed object on roadsides and road-shoulders
>
> would impose potential liability on public and private landowners
>
> for collisions occurring whenever a vehicle was driven off-road and
>
> into the object.” Turner at ¶ 23, quoting Ramby at *3. See also Floering v. Roller, 6th Dist. Wood No. WD-02-076, 2003-Ohio-5679, ¶ 18 (landowner owed no duty to motorist who struck a tree in the right-of-way, because the tree did not obstruct the motorist’s vision and could “only be a hazard when a vehicle leaves the highway”).
>
> {¶ 26} Here, the Burrs’ mailbox did not render ordinary travel on the regularly traveled portion of Young Road unsafe. To the extent the mailbox presented a hazard to motorists, it did so only with respect to those motorists who errantly left the road.
>
> C. An adjacent landowner or occupier of land adjacent to a public road

<details><summary>Other passages available</summary>

`cl11419421:12`

> Our negligent hiring cases ordinarily involve injuries to members of the public, patients, customers, or others exposed to the tortfeasor because of the defendant's hiring or retention decision. See, e.g., Theisz v. Massachusetts Bay Transp. Auth., 495 Mass. 507, 517-519 (2025) (members of public); Roe No. 1 v. Children's Hosp. Med. Ctr., 469 Mass. 710, 714 (2014) (patients); Foster v. The Loft, Inc., 26 Mass. App. Ct. 289, 291 (1988) (customers). This case is different. The plaintiff's exposure to MBT did not flow from the defendant's hiring decision. MBT, not the defendant, hired the plaintiff, directed his day-to-day work, supplied the fall protection equipment, and controlled the manner in which that equipment was used. See Hancock, 480 Md. at 610. To treat the defendant's selection of MBT as the legal source of a duty to MBT's own employees would collapse the line between a duty to protect persons foreseeably exposed to a contractor's negligence and a duty to protect the contractor's own employees from risks inherent in the work itself.
>
> Moreover, the plaintiff is not left without a remedy for his injuries. He filed a workers' compensation claim through MBT's insurer, administered by the New York State Workers' Compensation Board. See Carney v. Union Pac. R.R. Co., 2016 IL 118984, ¶ 84 (receipt of workers' compensation benefits assures remedy to injured person). Workers' compensation laws reflect a legislative compromise. They provide compensation for workplace injuries without requiring proof of fault, see Wright's Case, 486 Mass. 98, 114 (2020), but they also require employees to give up their common-law rights to recover against their employer, see G. L. c. 152, § 24.8
>
> Although the defendant was not the plaintiff's employer, recognizing a duty here would put the common law in tension with the exclusivity of workers' compensation. That is particularly true where, as here, the subcontract contains an indemnification provision requiring the subcontractor to compensate the general contractor for its loss arising from the subcontractor's work.

`cl9556163:10`

> On review of the summary judgment record, we conclude that the execution-style murder that occurred here was not a reasonably foreseeable risk that UTP had the ability to prevent, and therefore, UTP had no duty to protect the decedent against this sudden, unanticipated act of violence. To begin, there was no evidence "that the defendant was affiliated in any way with, or knowledgeable about, the [perpetrator] or any dispute that the [perpetrator] may have had with the [decedent]." Belizaire, 88 Mass. App. Ct. at 305. Rather, the record suggests that the shooting was not related in any way to Phan, UTP, the property, or City Limits, and that it only occurred there because the perpetrator happened upon the decedent there that evening.
>
> Of course, UTP's duty is not circumscribed by what it knew; the duty also encompasses what it should have known. The plaintiff relies heavily on the evidence of prior acts of violence at the property to argue that the harm that occurred here was reasonably foreseeable. However, even if UTP should have known of the prior acts of violence identified by the plaintiff, that would not be conclusive on the question of duty. Whittaker, 418 Mass. at 199. See Mullins v. Pine Manor College, 389 Mass. 47, 56 (1983), citing Samson v. Saginaw Professional Bldg., Inc., 393 Mich. 393, 406–407 (1975) ("Prior criminal acts are simply one factor among others that establish the foreseeability of the act of [a] third party"). We must also consider whether the harm that the plaintiff claims was foreseeable is one "that the defendant has an ability to prevent." Heath-Latson, 487 Mass. at 584. Here, the record cannot reasonably support a conclusion that security measures, including those suggested by the plaintiff's expert, such as additional exterior lighting and an additional security presence near the nightclub's exit, would have prevented the shooting that occurred.9 See Petrell, 453 Mass. at 381. To the contrary, the record indicates that despite the presence of security staff at the nightclub and, specifically, on duty at the entrance

`cl5129137:12`

> {¶ 23} Akin to the facts here, Turner involved a motorist’s off-road collision with a stationary, man-made object in the right-of-way. In Turner, an automobile passenger died when the driver inadvertently drove off the road in darkness and fog and struck a utility pole located in a grassy portion of the right-of-way. The administrator of the passenger’s estate sued the utility companies for negligently placing, maintaining, and using the utility pole in such close proximity to the road. This court held that the trial court properly granted summary judgment in favor of the utility companies on the plaintiff’s negligence claim.
>
> January Term, 2021
>
> {¶ 24} Although Turner involved the duty of public utilities vis-à-vis the placement of a utility pole, we noted that our holding in that case was consistent with “the approach that we have taken regarding liability of political subdivisions and private landowners for injuries caused by objects within the right-of-way of the road,” id. at ¶ 22, citing Strunk v. Dayton Power & Light Co., 6 Ohio St.3d 429, 453 N.E.2d 604 (1983), and Manufacturer’s, 63 Ohio St.3d 318, 587 N.E.2d 819. We reiterated that the focus, with respect to the duties owed to motorists by political subdivisions and by private landowners or occupiers, is not on the location of an off-road object but on whether that object “makes the roadway unsafe for the usual and ordinary course of travel.” (Emphasis sic.) Id. And we held that “when a vehicle collides with a utility pole located off the improved portion of the roadway but within the right-of-way, a public utility is not liable, as a matter of law, if the utility has obtained any necessary permission to install the pole and the pole does not interfere with the usual and ordinary course of travel.” Id. at ¶ 21. See also Link at ¶ 39 (“Absent evidence of interference with the usual and ordinary course of travel on the roadway, [the utility companies] did not have a duty to remove off-road objects within the public right-of-way that might come in contact with wayward vehicles”).

`cl5129137:14`

> does not owe a duty of care to motorists with respect to a hazard
>
> in the right-of-way that does not affect the safety
>
> of the ordinary course of travel on the road
>
> {¶ 27} Despite this court’s consistent holdings that an adjacent landowner or an occupier of land adjacent to a public road owes no duty to motorists regarding an off-road hazard that does not affect the safety of ordinary on-road travel, the Snays encourage us to recognize an exception to that rule. They argue that Burr’s
>
> January Term, 2021 “unreasonably dangerous construction” of his mailbox, with knowledge that the construction was inconsistent with the nonbinding guidelines published by the United States Postal Service, gave rise to a duty of care to motorists who might foreseeably leave the road and strike the mailbox.
>
> {¶ 28} As support for their proposed exception, the Snays cite a footnote from Ramby. After the Second District determined in Ramby that the city of Beavercreek did not have a duty to remove an off-road hazard that rendered only off-road travel unsafe, 2d Dist. Greene No. 93-CA-52, 1994 WL 124829 at *3, the appellate court stated that the plaintiff had identified no authority for subjecting the adjacent landowner to a greater duty to maintain the right-of-way free from nuisance than that imposed upon the city to which the right-of-way had been dedicated, id. at *5. In a footnote, however, the court noted: “The only distinction we can envision would be if the owner of the adjacent property had actual or constructive knowledge of the nuisance, while the municipality had no such notice.” Id. at fn. 2.

</details>

| | Label | Reason |
|---|---|---|
| Rater A | `supported` | Step 1: cl5129137:13 says the court 'cited with approval Ramby v. Ping' and quotes its rationale that otherwise 'every tree and solid fixed object on roadsides' would impose potential liability. |
| Rater B | `supported` | cl5129137:13 says the court cited Ramby with approval and quotes its rationale that otherwise every tree and solid fixed object on roadsides would create potential liability. |

**Recommended:** `supported` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] patent_obviousness-cc-4 · citation_check · Elekta Limited v. Zap Surgical Systems, Inc. (cafc, 2023-09-21)

Source: [https://www.courtlistener.com/opinion/9427507/elekta-limited-v-zap-surgical-systems-inc/](https://www.courtlistener.com/opinion/9427507/elekta-limited-v-zap-surgical-systems-inc/) · opinion 9841132 · cited authority as it appears: `In re Gartside, 203 F.3d 1305, 1312`

**Claim:** An expert's conclusory testimony that a claimed feature was known in the prior art does not explain why a skilled artisan would have been motivated to combine the references.

**Cited passage:** `cl9841132:4`

> We review the Board’s legal conclusions de novo and its factual findings for substantial evidence. ACCO Brands Corp. v. Fellowes, Inc., 813 F.3d 1361, 1365 (Fed. Cir. 2016). Substantial evidence means “such relevant evi-dence as a reasonable mind might accept as adequate to support a conclusion.” In re Gartside, 203 F.3d 1305, 1312 (Fed. Cir. 2000) (citation omitted).
>
> Obviousness is a question of law with underlying fac-tual issues relating to the “scope and content of the prior art, differences between the prior art and the claims at is-sue, the level of ordinary skill in the pertinent art, and any objective indicia of non-obviousness.” Randall Mfg. v. Rea,
>
> 1 Elekta also moved during the proceeding to amend its claims. J.A. 2; J.A. 67–68; J.A. 71. The Board denied that motion. J.A. 71. Elekta does not challenge that denial on appeal. 8 ELEKTA LIMITED v. ZAP SURGICAL SYSTEMS, INC. 733 F.3d 1355, 1362 (Fed. Cir. 2013) (first citing KSR Int’l Co. v. Teleflex Inc., 550 U.S. 398, 406 (2007); then citing Graham v. John Deere Co. of Kansas City, 383 U.S. 1, 17– 18 (1966)). Whether a skilled artisan would have been mo-tivated to combine references or would have had a reason-able expectation of success in combining references are questions of fact reviewed for substantial evidence. Re-gents of Univ. of California v. Broad Inst., Inc., 903 F.3d 1286, 1291 (Fed. Cir. 2018).
>
> DISCUSSION
>
> On appeal, Elekta makes three principal arguments: that the Board’s findings on a motivation to combine are unsupported by substantial evidence, Appellant’s Br. 26; that the Board failed to make any findings, explicit or im-plicit, on a reasonable expectation of success, id. at 4, 18; and that even had the Board made such findings, those findings are not supported by substantial evidence, id. at 2.
>
> I
>
> We first address Elekta’s argument that a skilled arti-san would not have been motivated to combine prior art references disclosing radiation imagery with the references disclosing radiation therapy. Appellant’s Br. 26.

<details><summary>Other passages available</summary>

`cl9954963:9`

> The only evidence presented by Aligned Vision in sup-port of a motivation to combine was the testimony of Dr. Mohazzab. With respect to claim 3, Dr. Mohazzab testified ’094 Rueb discloses a camera with a multi megapixel sen-sor and a skilled artisan “would also have known to use a camera with a multi megapixel sensor in mid-2016.” J.A. 825–26 ¶ 72. This conclusory testimony fails to address why or whether a skilled artisan would have been moti-vated to combine the camera disclosed in ’094 Rueb with Keitler and Briggs. Aligned Vision similarly failed to pre-sent any evidence as to why a skilled artisan would have been motivated to combine the teachings of ’094 Rueb with the other references to meet the subject matter of claims 4, 6, 8, and 9.
>
> We conclude substantial evidence supports the Board’s findings that Aligned Vision failed to show a motivation to combine for both Grounds 2 and 4. We affirm the Board’s determination that Aligned Vision failed to prove claims 3, 4, 6, 8, and 9 of the ’734 patent would have been obvious.
>
> CONCLUSION
>
> We reverse the Board’s determination that claims 1, 2, 5, 7, and 10–13 of the ’734 patent would have been obvious. We affirm the Board’s determination that Aligned Vision failed to prove claims 3, 4, 6, 8, and 9 would have been ob-vious. AFFIRMED IN PART AND REVERSED IN PART
>
> COSTS Costs awarded to Virtek.

`cl9841132:12`

> Elekta misstates the applicable burden of proof. See id. In an IPR, the petitioner bears the burden in the peti-tion to demonstrate by a preponderance of the evidence that the challenged patent (or portions thereof) is un-patentable. See 35 U.S.C. § 316(e) (“In an inter partes re-view instituted under this chapter, the petitioner shall have the burden of proving a proposition of unpatentability by a preponderance of the evidence.”). Apart from its ELEKTA LIMITED v. ZAP SURGICAL SYSTEMS, INC. 15 erroneous statement of the law, Elekta further failed to de-velop an argument concerning ZAP’s correct burden of proof. See Reply 11–13. We therefore deem this argument frivolous and waived. See Monsanto Co. v. Scruggs, 459 F.3d 1328, 1341 (Fed. Cir. 2006).
>
> CONCLUSION
>
> We have considered Elekta’s other arguments and find them unpersuasive. We hold that the Board’s findings on a motivation to combine and its implicit finding on a rea-sonable expectation of success are supported by substantial evidence. We affirm.
>
> AFFIRMED
>
> COSTS No costs.

`cl9841132:5`

> Obviousness requires, inter alia, a finding that a skilled artisan would have been motivated to combine the teachings of prior art in such a way that the combination discloses the claimed limitations. See OSI Pharms., LLC v. Apotex Inc., 939 F.3d 1375, 1382 (Fed. Cir. 2019). The inquiry into the existence of a motivation to combine as-sumes that a skilled artisan is a person of ordinary creativ-ity with common sense, common wisdom, and common knowledge. See Fleming v. Cirrus Design Corp., 28 F.4th 1214, 1223 (Fed. Cir. 2022). Thus, an obviousness deter-mination does not always require prior art to expressly state a motivation for every obvious combination. See, e.g., ELEKTA LIMITED v. ZAP SURGICAL SYSTEMS, INC. 9 id. Nor does an obviousness showing “require that a par-ticular combination must be the preferred, or the most de-sirable, combination described in the prior art in order to provide motivation for the current invention.” Novartis Pharms. Corp. v. West-Ward Pharms. Int’l Ltd., 923 F.3d 1051, 1059 (Fed. Cir. 2019) (citation omitted).
>
> Elekta contends that “[n]o substantial evidence sup-ports the Board’s finding that there was a motivation to combine these references by replacing the X-ray imaging source in Grady with a linac therapeutic source as proposed in the Petition,” because the linac “ionising radiation source [would] not offer any imaging improvement and also requires extreme precision due to its potentially lethal side effects.” Appellant’s Br. 29, 31. According to Elekta, the Grady device is for imaging and does not contemplate a heavy linac or account for the lack of precision that would result from the linac’s additional weight. Id. at 30–31.

`cl10759655:8`

> “Obviousness is a question of law with underlying factual issues . . . .” Elekta Ltd. v. ZAP Surgical Sys., Inc., 81 F.4th 1368, 1373–74 (Fed. Cir. 2023). The “test for obviousness is not . . . that the claimed invention must be expressly suggested in any one or all of the references. Rather, the test is what the combined teachings of the references would have suggested to those of ordinary skill in the art.” MCM Portfolio LLC v. Hewlett-Packard Co., 812 F.3d 1284, 1294 (Fed. Cir. 2015) (quoting In re Keller, 642 F.2d 413, 425 (CCPA 1981)). “[T]here must exist a motivation to combine various prior art references in order for a skilled artisan to make the claimed invention.” Virtek Vision Int’l ULC v. Assembly Guidance Sys., Inc., 97 F.4th 882, 887 (Fed. Cir. 2024). “Whether a skilled artisan would have been motivated to combine references” is a “question[] of fact reviewed for substantial evidence.” Elekta, 81 F.4th at 1374. “Substantial evidence is such relevant evidence as a reasonable mind might accept as adequate to support a conclusion.” Meridian Prods., LLC v. United States, 851 F.3d 1375, 1381 (Fed. Cir. 2017) (citation omitted). Although “we review decisions, not opinions, . . . a Board opinion must contain sufficient findings and reasoning to 10 PALO ALTO NETWORKS, INC. v. CENTRIPETAL NETWORKS, LLC permit meaningful appellate scrutiny.” Gechter v. Davidson, 116 F.3d 1454, 1458 (Fed. Cir. 1997).
>
> I
>
> The parties disagree on whether the Board found a motivation to combine Paxton and Sutton, and what the Board meant when it said that “the necessary bridge” was missing. PAN argues that “the Board did not dispute that a motivation existed to combine Paxton and Sutton,” Appellant’s Br. 3, and that “the Board[] [improperly] search[ed] for a ‘bridge’ within the confines of Paxton and Sutton,” Appellant’s Br. 37. Centripetal asserts that the Board found that “PAN established no motivation to combine,” Appellee’s Br. 38, and that “PAN had not established ‘the necessary bridge’ between the prior art and the claimed limitation,” Appellee’s Br. 34.

</details>

| | Label | Reason |
|---|---|---|
| Rater A | `wrong_document` | Step 3: the cited cl9841132:4 states the standard of review and the factual underpinnings of obviousness; the conclusory-expert-testimony point is in cl9954963:9, a different opinion. |
| Rater B | `wrong_document` | Cited cl9841132:4 is standard of review; cl9954963:9 (different opinion) says Mohazzab's conclusory testimony fails to address why a skilled artisan would be motivated to combine. |

**Recommended:** `wrong_document` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] qi_excessive_force-qa-4 · qa_citation · Santander v. Salazar (ca5, 2025-04-04)

Source: [https://www.courtlistener.com/opinion/10373064/santander-v-salazar/](https://www.courtlistener.com/opinion/10373064/santander-v-salazar/) · opinion 10839652 · cited authority as it appears: `Harmon v. City of Arlington, Texas, 16 F.4th 1159, 1167 (5th Cir. 2021)`

**Question:** In Santander v. Salazar, why did the Fifth Circuit describe the clearly established inquiry as especially demanding for excessive force claims, and what conduct did it say was clearly established as excessive?

**Reference notes:** Must mention: excessive force outcomes depend heavily on facts, so officers get immunity unless precedent squarely governs; it is clearly established that striking a suspect who is not resisting arrest is excessive.

**Chunks either rater chose:**

`cl10839652:8`

> “The clearly established inquiry is [especially] demanding” for excessive force claims. Harmon v. City of Arlington, Texas, 16 F.4th 1159, 1167 (5th Cir. 2021) (citing Morrow v. Meachum, 917 F.3d 870, 874 (5th Cir. 2019)). Because excessive force “is an area of the law ‘in which the result depends very much on the facts of each case,’ . . . police officers are entitled to qualified immunity unless existing precedent ‘squarely governs’ the specific facts at issue.” Kisela v. Hughes, 584 U.S. 100, 104–05 (2018) (per curiam) (quoting Mullenix, 577 U.S. at 13).
>
> Relevant here, it is clearly established that “officers engage in excessive force when they physically strike a suspect who is not resisting arrest.” Spiller v. Harris Cnty., Texas, 113 F.4th 573, 578 (5th Cir. 2024); see also Carroll v. Ellington, 800 F.3d 154, 177 (5th Cir. 2015) (“The law was clearly established at the time of the deputies’ conduct that, once a suspect has been handcuffed and subdued, and is no longer resisting, an officer’s subsequent use of force is excessive.”). Though Santander’s complaint does not illuminate the nature of the “verbal conversation” between Santander and Texas Republic staff that led to his altercation with Salazar, Santander alleges that he had turned to “go to a different set of stairs” before being “violently shoved” in the back “suddenly and without provocation.” Salazar thus initiated the physical confrontation when Santander had his back turned and was not resisting. Salazar’s doing so, if proven, would violate a clearly established right based on the above precedents. And because the initial shove alone supports a plausible excessive force claim, we need not further assess at the pleadings stage whether excessive force was present for
>
> No. 24-10275 the whole encounter. Cf. Lytle v. Bexar County, 560 F.3d 404, 413 (5th Cir. 2009) (“An exercise of force that is reasonable at one moment can become unreasonable in the next if the justification for the use of force has ceased.”). Accordingly, this claim survives Salazar’s Rule 12(b)(6) motion and his assertion of qualified immunity.
>
> 2.

Candidate window: `cl10839652:6`, `cl10839652:7`, `cl10839652:8`, `cl10839652:9`, `cl10839652:10`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl10839652:8']` | cl10839652:8 gives the fact-dependence rationale and the clearly established rule on striking a non-resisting suspect. |
| Rater B | `['cl10839652:8']` | cl10839652:8 says the inquiry is especially demanding for excessive force, immunity unless precedent squarely governs, and that striking a non-resisting suspect is clearly established excessive force. |

**Recommended:** `['cl10839652:8']` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---

### [ ] title_vii_retaliation-qa-2 · qa_citation · Ayorinde v. Team Industrial (ca5, 2024-11-08)

Source: [https://www.courtlistener.com/opinion/10270600/ayorinde-v-team-industrial/](https://www.courtlistener.com/opinion/10270600/ayorinde-v-team-industrial/) · opinion 10737190 · cited authority as it appears: `Aryain v. Wal-Mart Stores Texas LP, 534 F.3d 473, 480 (5th Cir. 2008)`

**Question:** Why did the Fifth Circuit in Ayorinde v. Team Industrial Services hold that Ayorinde failed to exhaust his constructive discharge claim?

**Reference notes:** Must mention: neither EEOC charge contained allegations like or related to constructive discharge; the resignation letter has no bearing on exhaustion; the charges made no reference to his resignation or to intolerable conditions.

**Chunks either rater chose:**

`cl10737190:7`

> Despite challenging the district court’s conclusion, Ayorinde offers no discussion of his allegations before the EEOC, instead highlighting the allegations made in his letter of resignation. Ayorinde’s letter of resignation has no bearing on whether he exhausted his administrative remedies. Neither Ayorinde’s original EEOC charge nor his amended charge includes allegations “like or related to” his constructive discharge claim. Although Ayorinde asserted that he was discriminated against on the basis of his race and age because his supervisor failed to schedule him for jobs, he did not allege facts suggesting his “working conditions [became] so intolerable that a reasonable person in [Ayorinde’s] position would have felt compelled to resign.” Aryain v. Wal-Mart Stores Texas LP, 534 F.3d 473, 480 (5th Cir. 2008) (first alteration in original) (quoting P a. State Police v. Suders, 542 U.S. 129, 141 (2004)). Indeed, Ayorinde made no reference at all to his resignation in either of his EEOC charges. We thus conclude that Ayorinde has failed to exhaust administrative remedies with respect to his constructive discharge claim and that summary judgment was proper.
>
> Lastly, Ayorinde argues that he has established a prima facie hostile work environment claim based on “racial harassment. ” To establish a prima facie case for a race-based hostile work environment claim, a plaintiff must show: “(1) [he] belongs to a protected group; (2) [he] was subjected to unwelcome harassment; (3) the harassment complained of was based on race; (4) the harassment complained of affected a term, condition, or privilege of employment; (5) the employer knew or should have known of the harassment in question and failed to take prompt remedial action.” Arredondo v. Elwood Staffing Servs., Inc., 81 F.4th 419, 433 (5th Cir. 2023) (quoting Ramsey v. Henderson, 286 F.3d 264, 268 (5th Cir. 2002)). “Harassment generally takes the form of ‘discriminatory intimidation, ridicule, and insult’ that rises to the level of ‘hostile or abusive.’” Clark v. City of Alexandria, 116 F.4th 472, 479

Candidate window: `cl10737190:5`, `cl10737190:6`, `cl10737190:7`, `cl10737190:8`, `cl10737190:9`

| | Label | Reason |
|---|---|---|
| Rater A | `['cl10737190:7']` | cl10737190:7 explains the charges lacked related allegations and that the resignation letter is irrelevant. |
| Rater B | `['cl10737190:7']` | cl10737190:7 says neither charge had allegations like or related to constructive discharge, the resignation letter has no bearing, and the charges never referenced resignation. |

**Recommended:** `['cl10737190:7']` — Confirm: the agreed label matches the passage on a re-read.

**Final label:** ______

---
