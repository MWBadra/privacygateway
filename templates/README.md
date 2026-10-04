# Egyptian bank document templates: catalog

All files are public, blank bank documents downloaded from the banks' own sites on 2026-10-02.
None contain customer data. Use for structure and layout study only. Do not redistribute.
Previews (PNG) are in `previews/`.

| # | Category | Files | What it is |
|---|---|---|---|
| 1 | Account opening / KYC forms | 7 | Short fill-in forms: labelled boxes, checkboxes, dotted lines |
| 2 | Transaction request forms | 3 | One-page forms: transfer, card dispute, supplementary card |
| 3 | Contracts and terms | 5 | Long legal prose with blanks for names, IDs, amounts, dates |
| 4 | Tariffs, guides, info | 3 | Tables, FAQs, UI screenshots |
| 5 | Financial reports | 1 | Notes to financial statements (EN translation, 66 pages) |
| 9 | Unusable as-is | 3 | Placeholder or broken-encoding PDFs (kept as negative tests) |

## 1_account_opening_kyc_forms
| File | Bank | Language | Notes |
|---|---|---|---|
| nbe_account_opening_individuals_ar.pdf | NBE | Arabic (+ "English Name" field) | 5 pp, RTL form, income bands, occupation, residency, related parties |
| kfh_egypt_account_opening_bilingual.pdf | Ahli United Bank (now KFH Egypt) | Bilingual side by side | 22 pp, character-box fields (ID number, mobile, dates) |
| hsbc_personal_account_opening_en.pdf | HSBC Egypt | Bilingual EN/AR | 7 pp, 10 MB |
| hsbc_additional_account_en.pdf | HSBC Egypt | Bilingual | 1 p, existing customers |
| hsbc_youth_account_opening_ar.pdf | HSBC Egypt | Arabic | 6 pp, 10 MB |
| hsbc_premier_children_ar.pdf | HSBC Egypt | Arabic/EN | 7 pp |
| hsbc_nonresident_savings_cert_bilingual.pdf | HSBC Egypt | Bilingual | 2 pp, account number in boxes (EG HKEB...) |

## 2_transaction_request_forms
| File | Bank | Notes |
|---|---|---|
| hsbc_internal_transfer_request_en.pdf | HSBC | Debit/credit account, amount, amount in words, reason, signature, "for bank use only" |
| hsbc_cardholder_dispute_bilingual.pdf | HSBC | Card no., transaction table (date, merchant, amount), checkbox reasons |
| hsbc_supplementary_credit_card_bilingual.pdf | HSBC | 4 pp, applicant and supplementary-holder details |

## 3_contracts_and_terms
| File | Bank | Language | Notes |
|---|---|---|---|
| nbe_personal_loan_agreement_ar.pdf | NBE | Bilingual two-column | 12 pp, parties, ID, amount, branch manager, clauses |
| hsbc_personal_finance_application_bilingual.pdf | HSBC | Bilingual | 10 pp |
| bdc_qcash_terms_bilingual.pdf | Banque du Caire | Arabic | 13 pp, wallet T&Cs |
| aaib_account_booklet_individuals_en.pdf | AAIB | English | 11 pp, long prose |
| aaib_account_booklet_corporate_en.pdf | AAIB | English | 24 pp |

## 4_tariffs_guides_info
| File | Bank | Notes |
|---|---|---|
| nbe_tariff_individuals.pdf | NBE | English tariff tables (fees, limits) |
| banquemisr_iban_en.pdf | Banque Misr | Explains the 29-character Egyptian IBAN |
| banquemisr_money_transfer_ar.pdf | Banque Misr | Corporate online banking guide: screenshots of transfer screens (34 pp) |

## 5_financial_reports
| File | Notes |
|---|---|
| nbe_financial_statements_translation.pdf | Dense English notes, little text layer: needs OCR |

## 9_unusable
| File | Why |
|---|---|
| hsbc_kyc_form_en.pdf | XFA form: opens as "requires Adobe Reader" placeholder |
| hsbc_complaint_form_en.pdf | Same: XFA placeholder |
| hsbc_savings_certificates_en.pdf | Arabic font encoding is garbled in the text layer (good negative test) |

## Not obtained
- **CIB**: the site blocks automated downloads (bot protection). Forms must be downloaded by hand in a browser:
  https://www.cibeg.com/en/risk-and-responsibility/customer-information-update
- **Customer account statements, transfer receipts, cheques, loan schedules**: no bank publishes a real sample. The only "templates" found are on Scribd, and they are forgery kits for fake proof-of-address documents, so they were not used.
- Banque Misr credit card form, QNB, Banque du Caire, Alexbank, ADIB, Faisal, Credit Agricole: no direct PDF forms found via search; most are web forms.

## Finding: text extraction from these PDFs is already broken
Extracting text with PyMuPDF/pypdf shows damage that a generator has to reproduce:
- NBE form: "للأفراد" comes out as "لألفراد", "البيانات الأساسية" as "ات األساسية", and the colon moves to the wrong side.
- Banque du Caire: letters come out as Arabic presentation forms (U+FExx) in visual order.
- HSBC savings certificate: Arabic comes out as Greek-looking glyphs ("ΏϠρ").
- HSBC internal transfer: Arabic and English labels are fused on the same line without a separator.
