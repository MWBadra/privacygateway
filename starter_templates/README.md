# Starter templates (3)

Chosen as the most Arabic-focused documents with a usable text layer, one per document family.
Source files are public blank documents (copies of those in `../templates` and `../banque_misr`).

| | File | Family | Arabic share | Pages | Why |
|---|---|---|---|---|---|
| T1 | T1_nbe_account_opening_individuals_ar.pdf | Fill-in form | 99% | 5 (2 form + 3 dense terms) | Pure Arabic, RTL form, dozens of fields, dense legal Arabic on pp 3-5 |
| T2 | T2_nbe_personal_loan_agreement_bilingual.pdf | Contract | 48% | 12 | Arabic and English columns, PII embedded in prose, amounts, dates, checkboxes |
| T3 | T3_banque_misr_online_transfer_guide_ar.pdf | Transaction screens | 100% | 34 | Only Arabic-only Banque Misr (Egypt) document: transfer / beneficiary / card-payment screens |

Previews are in `previews/` (T1 p1-2, T2 p1 and p12, T3 p9 and p12).

## T1: NBE account opening, individuals (Arabic form)
Fields (from the real text): request no., branch, date; full name (Arabic) and English name; CIF no.; printed no.; ID type and no.; issued by; gender; issue and expiry dates; date, place and country of birth; nationality and other nationalities; customer type; disability; housing type; permanent address and country; mailing address; statement frequency, method and language; home phone, mobile 1 and 2 with country codes; email; employment type, profession, job title, employer name, start date, employer address and phone; income sources; annual income band; PEP / beneficial-owner / power-of-attorney / other-bank questions; marital status; residency; education; co-operators table (CIF, name, capacity, document); account purpose, expected volume, type, currency; debit card name to print; e-wallet mobile number; consent.
- PII value types needed: Arabic name + Latin name, 14-digit national ID, CIF, dates, phone, email, address, employer.
- Structure: Arabic-only labels, ticks, tables, 1.5 pages of fields then 3 pages of legal terms.

## T2: NBE personal cash loan against Al Ahly Plus certificate (bilingual contract)
Content: date written in words ("حرر هذا ... الموافق"), bank representative and branch manager names, borrower name, residence, national ID or passport no. with date and issuer, loan amount in digits **and in words**, certificate numbers and values, loan account no., purpose checkboxes, term and instalment dates, instalment frequency, repayment clauses, final declaration (other debts, related parties).
- PII value types needed: names, 14-digit ID, account no., amounts, dates, branch.
- Hard cases built into it: number next to "رقم" vs next to "جنيه" (identifier vs amount), amounts in words, dates split into three blanks, two columns where Arabic and English duplicate the same blank.

## T3: Banque Misr online banking, transfers (Arabic guide)
Screens and field descriptions for: own-account transfer, third-party transfer, recurring transfer, card payment, local-bank card payment (ACH). Fields: source account, beneficiary, card number, amount, transfer reason, fee bearer, notes, transaction date, frequency. This is a manual, so it has no filled values.
- To use it we have to **derive** an instance document from the screens (a transfer confirmation / instruction), and that derivation is a design decision for us, not something copied from the bank.
- Runner-up if you want a real form instead: the bilingual Banque Misr UAE Money Transfers Form (`../banque_misr/uae_branch/money_transfer_application_form.pdf`). It is only 41% Arabic and its Arabic text layer is damaged.

## Finding: the text layer corrupts Arabic in a regular, reproducible way
Confirmed on T1, T2 and T3. When a lam is followed by alef (or hamza-alef), the extracted text swaps the two letters:

| Real word | Extracted |
|---|---|
| الميلاد (birth) | الميالد |
| الصلاحية (validity) | الصالحية |
| الإقامة (residence) | اإلقامة |
| الأهلي (Ahly) | األهلي |
| للأفراد (for individuals) | لألفراد |
| الأموال (funds) | األموال |

In T1, correct spellings appear 0 times and swapped spellings appear (الميالد 3, اإلقامة 4, األهلي 36, اإللكتروني 31).
Consequences:
- A name like **عبد الله** would likely extract as **عبد اهلل**, and **إسلام**, **إيمان**, **الإسكندرية** would change too. A name detector and a regex written against the clean strings will miss these.
- Punctuation also moves: ":التاريخ" instead of "التاريخ:".
- The generator can model this with one rule (swap lam and alef-variant) applied to the text layer, not to the visible rendering.

## What the three templates imply for the generator
| Need | T1 | T2 | T3 |
|---|---|---|---|
| Arabic + Latin name pairs | yes | yes | no |
| 14-digit national ID with embedded date and governorate | yes | yes | no |
| Account no. / CIF / IBAN | yes | yes | yes |
| Dates (Arabic-Indic and Western digits) | yes | yes (split in 3 blanks) | yes |
| Phone / email / address | yes | partly | no |
| Amounts in digits and in Arabic words | no | yes | yes |
| Narrative prose around PII | little | yes | little |
| Lam-alef extraction corruption | yes | yes | yes |
So a names-and-numbers lookup table covers T1 and the identifier parts of T2. T2 additionally needs an Arabic number-to-words routine and grammatical agreement in the prose, and T3 needs a decision about what a filled instance looks like.
