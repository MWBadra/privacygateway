# Banque Misr documents: scan report

41 public, blank Banque Misr PDFs, downloaded 2026-10-02. No customer data.
Machine-readable scan results: `scan.json`. First-page previews: `previews/`.

Two subfolders, because they are different legal entities and different jurisdictions:

- `egypt/` (16 files): from banquemisr.com, the Egyptian bank. **Tariffs, rates, limits, guides.** The site publishes almost no fill-in forms.
- `uae_branch/` (25 files): from banquemisr.ae, Banque Misr UAE (licensed by the UAE central bank). **Real application forms, KYC, contracts.** Same brand, same bilingual layout style, but UAE content: AED, Emirates ID (EID), UAE addresses. Use it as a layout and field-structure reference, not as Egyptian data.

## Egypt (banquemisr.com)

| File | Type | Pages | Language | Text layer | Notes |
|---|---|---|---|---|---|
| corporate_client_info_form_en | Form | 1 | EN | yes | The only fill-in form on the Egyptian site: client name, ID card no. (14 boxes), phone, company account no. (character boxes), last withdrawal/deposit |
| bm_online_business_guide_ar | UI guide | 34 | AR | yes (3 image-only pages) | Screenshots of the corporate online-banking screens: transfer, standing orders, beneficiaries. Arabic text only. Highlights show where fields sit |
| schedule_of_charges_individual_en | Tariff | 4 | EN | yes | Fee tables, effective 1 Jul 2026 |
| fees_individual_accounts_en | Tariff | 1 | EN | yes | |
| fees_day_by_day_en | Tariff | 1 | EN | yes | Mutual-fund account fees |
| corporate_tariff_en | Tariff | 12 | EN | yes | |
| credit_card_limits_fees_en | Tariff | 7 | EN | yes | Card fees and limits |
| card_usage_outside_egypt_en | Limits | 2 | EN | yes | |
| bm_online_transfer_limits_individuals_en | Limits | 1 | EN | yes | |
| interest_rates_individuals_en | Rates | 18 | EN | yes (1 image-only page) | |
| interest_rates_corporate_en | Rates | 5 | EN | yes | |
| islamic_deposit_returns_en | Rates | 10 | EN | yes | |
| cd_redemption_instructions_en | Table | 2 | EN | **none (0 chars)** | Text is drawn as vector outlines: needs OCR |
| iban_explainer_en | Info | 2 | EN | yes | Egyptian IBAN: EG + 2 check + 4 bank + 4 branch + account |
| customer_rights_protection_en | Info | 1 | EN | yes | |
| custody_fees_en | Tariff | 3 | EN | yes | |

## UAE branch (banquemisr.ae)

| Category | Files | Fillable fields | Notes |
|---|---|---|---|
| Personal forms | money_transfer_application_form (1 p, 37 fields), debit_card_application_form (2 pp, 31), e_service_form_individual (3 pp, 15), credit_card_application_secured (6 pp, none), personal_loan_vs_term_deposit_form (2 pp), overdraft_application_form (2 pp), term_deposit_application_form (2 pp), pearl_savings_addendum_form (1 p), letter_of_pledge (2 pp) | mixed | Fully bilingual EN/AR, label pairs side by side |
| KYC | re_kyc_individual_non_us (7 pp, 197 fields), re_kyc_entities_non_us (24 pp, 443 fields) | yes | The richest source of PII field types: name as per EID, EID no. boxes, passport, nationality, mother's name, address, income, source of wealth |
| Business forms | lc_issuance_application (4 pp, 135 fields), lg_issuance_application (3 pp, 64), specialized_chequebook_request (2 pp, 34), business_debit_card_request (3 pp, 25), business_eservice_subscription (1 p, 24) | yes | Trade-finance and cheque forms |
| Contracts and terms | general_terms_conditions (98 pp), general_terms_conditions_v1 (99 pp), credit_card_terms (11 pp), personal_loan_terms (3 pp), business_account_opening_terms (10 pp), swift_services_terms (6 pp) | none | Long legal prose |
| Statements and guides | kfs_individual_accounts (3 pp), kfs_non_individual_accounts (1 p), online_banking_user_guide_individual (6 pp) | none | Key Facts Statements |

## Findings that matter for the data

1. **The layout style is consistent across Banque Misr forms.** Bilingual, right-to-left Arabic label mirrored against an English label, shaded section headers, character boxes for IDs and account numbers, tick boxes, a "For Bank Use Only" strip with Reference No., Value Date, Maker, Checker and Exchange Rate. One well-built template engine could reproduce all of them.
2. **Fields the forms contain:** customer name (Arabic and Latin), ID number (EID boxes), passport no., nationality, date and place of birth, mother's name, address, phone, email, occupation, income and source of wealth, account no. and IBAN, beneficiary name, address, bank and SWIFT, amount in figures and in words, currency, purpose of payment, signatory name, card numbers.
3. **Text extraction of the Arabic is broken in 20 of the 25 UAE PDFs** (the other five are English-only or have a clean Arabic layer). Arabic comes out as presentation-form glyphs (U+FExx) in visual order, and the Arabic and English labels are fused with no separator (for example `Branch Nameإﺳﻢ اﻟﻔﺮعDateاﻟﺘﺎرﻳﺦ`). This is the same failure seen in the earlier bank files. Any PDF-based benchmark has to be built from the *extracted* text, not from what we generate.
4. **Two PDFs are not extractable at all:** `cd_redemption_instructions_en` (outlined text) and some image-only pages in the guide and rate sheets. These need OCR.
5. **Some UAE forms are fillable PDFs (AcroForm).** Field names reveal the structure (`Beneficiary Account No IBAN No...`), but some names are mangled by font encoding (`Beniÿciary`).
6. **`general_terms_conditions_v1` is a clean bilingual contract.** 99 pages, about 110k Arabic letters with a normal Arabic text layer, which makes it a good source of real legal Arabic phrasing.
7. **What is still missing:** Egyptian retail account-opening, KYC, transfer or loan forms. The Egyptian site has only the online forms (credit-card application, "open your account online"), which are web pages, not PDFs. A real statement or receipt is not public.
