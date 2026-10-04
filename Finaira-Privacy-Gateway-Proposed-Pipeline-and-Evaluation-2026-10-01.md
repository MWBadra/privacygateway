# Finaira Privacy Gateway: Proposed Pipeline and Evaluation Plan

**Research date:** 1 October 2026  
**Purpose:** Convert the confirmed Finaira problem into a feasible, research-worthy system pipeline.  
**Status:** Research recommendation only. No architecture or technology below is a confirmed project decision.

## Executive recommendation

Build a **local privacy gateway around a cloud LLM**, not a new NER model and not a full enterprise privacy platform.

The recommended contribution is:

> A policy-driven, reversible privacy gateway that combines deterministic financial-identifier validation, Arabic/multilingual entity models, selective local contextual reasoning, scoped pseudonyms, and end-to-end privacy–utility evaluation for Arabic–English financial documents.

The strongest academic result would not be “we masked PII.” That pattern already exists in systems such as [HaS](https://arxiv.org/abs/2309.03057) and [Portcullis](https://ojs.aaai.org/index.php/AAAI/article/view/32088). The defensible contribution is the **Arabic–English financial adaptation, ambiguity resolution, token-scope design, benchmark, and end-to-end evaluation**.

## Confirmed project requirements

From the current Finaira project context:

- raw sensitive information must remain inside the trusted local environment;
- only a protected representation may cross into the external cloud environment;
- protection must be reversible for authorized users;
- Arabic, English, and mixed Arabic–English financial text must be supported;
- protected text must remain useful for retrieval, question answering, or related document tasks;
- privacy and utility must both be evaluated.

The following are still open: jurisdictions, document formats, entity taxonomy, cloud task, hardware, data availability, acceptable error rates, restoration scope, and whether OCR is required in the MVP.

## What the evidence implies

1. **A single detector is insufficient.** Microsoft Presidio deliberately combines NER, regex, rules, checksums, and context, and explicitly warns that automated detection cannot guarantee finding all sensitive information ([Presidio documentation](https://data-privacy-stack.github.io/presidio/)).
2. **Financial NER is not the same as PII detection.** [AMWAL](https://aclanthology.org/2025.finnlp-1.20/) reports strong performance on Arabic financial news, but its financial concepts do not cover the full privacy taxonomy and its domain differs from customer documents.
3. **Arabic resources help but do not solve the domain problem.** [Wojood](https://aclanthology.org/2022.lrec-1.387/) contains 550K Arabic tokens, 75K entities, and 21 entity types across multiple domains; it is useful for general Arabic entities, not a ready-made financial PII benchmark.
4. **Recent multilingual detectors are promising baselines, not proven solutions.** [GLiNER2-PII](https://arxiv.org/abs/2605.09973) is a 0.3B multilingual model covering 42 PII types at character-span resolution, but it was trained on a relatively small synthetic corpus. Arabic financial performance must be measured locally.
5. **Span recall alone does not establish privacy.** The [SPIA](https://aclanthology.org/2026.acl-long.778/) experiments found that high masking recall could still leave personal information inferable from context. [TAB](https://aclanthology.org/2022.cl-4.19/) likewise evaluates privacy-oriented annotations and co-reference rather than ordinary NER alone.
6. **Pseudonymization reduces risk; it is not anonymization.** Reversible data remains linkable through separately held information. The [EDPB pseudonymisation guidance](https://www.edpb.europa.eu/system/files/2025-01/edpb_guidelines_202501_pseudonymisation_en.pdf) emphasizes separating and protecting the additional information needed for attribution. [NIST SP 800-188](https://csrc.nist.gov/pubs/sp/800/188/final) recommends measurable de-identification standards and re-identification studies.
7. **Utility must be tested on the actual downstream task.** Prior work shows pseudonymization choices affect classification and summarization differently ([Yermilov et al., 2023](https://aclanthology.org/2023.trustnlp-1.20/)). Semantic similarity alone is therefore not sufficient.

## Proposed end-to-end pipeline

```text
                         TRUSTED LOCAL ENVIRONMENT

Document / query
      │
      ▼
[1] Parse + preserve layout/offsets ──► optional OCR
      │
      ▼
[2] Normalize for matching while retaining raw↔normalized offset map
      │
      ▼
[3] High-recall candidate detection
      ├─ structured rules + checksums
      ├─ multilingual PII model
      ├─ Arabic/general NER
      └─ Arabic financial NER
      │
      ▼
[4] Fusion + alias/coreference resolution
      │
      ├─ confident decision ─────────────────┐
      └─ uncertain high-risk span            │
                    │                        │
                    ▼                        │
          local contextual SLM               │
                    └────────────────────────┘
      │
      ▼
[5] Versioned policy: preserve / tokenize / generalize / remove / review
      │
      ▼
[6] Scoped typed tokens + encrypted local mapping vault
      │
      ▼
[7] Pre-egress leakage gate + data minimization
      │
══════╪══════════════════ TRUST BOUNDARY ═════════════════════
      ▼
[8] Cloud task on protected text: retrieval, QA, or summarization
      │
══════╪══════════════════ TRUST BOUNDARY ═════════════════════
      ▼
[9] Token-integrity validation + unexpected-PII scan
      │
      ├─ unsafe ─► block / retry / human review
      └─ safe
          │
          ▼
[10] Authorized local restoration + privacy-safe audit record
```

### 1. Local document preparation

**Recommended MVP:** begin with plain text and text-layer PDFs. Add scanned documents only after the text path is stable.

- Use a simple PDF parser as the control implementation; benchmark [Docling](https://docling-project.github.io/docling/getting_started/quickstart/) if layout, tables, or multiple document formats matter.
- Use OCR only for pages without a usable text layer. PaddleOCR has an Arabic–English recognition model, but it must be benchmarked on the actual document styles ([PaddleOCR multilingual documentation](https://www.paddleocr.ai/latest/en/version3.x/algorithm/PP-OCRv5/PP-OCRv5_multi_languages.html)).
- Preserve page, block, table-cell, and character-offset metadata.
- Normalize Arabic letter variants, whitespace, direction marks, and Arabic-Indic/Western digits **for matching only**. Maintain an offset map back to the exact original text.

Why this matters: an OCR or offset error can cause the system to mask the wrong substring even when the detector found the right entity.

### 2. High-recall candidate detection

Use complementary detectors with one common span schema:

```text
{start, end, raw_text, normalized_text, candidate_type,
 detector, score, evidence, page, block}
```

| Detector | Primary responsibility | Proposed implementation |
|---|---|---|
| Structured recognizers | IBAN, cards, phone, email, national/business IDs, known account/reference formats | Regex plus checksum/format validators; country rules only after target jurisdictions are confirmed |
| Multilingual PII model | Broad privacy-oriented span candidates | GLiNER2-PII as a current candidate baseline |
| Arabic general NER | PERSON, ORG, LOCATION and related Arabic spans | Wojood-trained model or another benchmarked Arabic NER model |
| Arabic financial NER | Banks and financial-domain context | AMWAL as a baseline and evidence source, not the final privacy classifier |
| Local contextual SLM | Resolve difficult numeric/contextual ambiguity | Called only for uncertain spans or blocks, with structured output |

Do **not** run a local generative model as the only detector. It is slower, its offsets can be unstable, and its confidence is not naturally calibrated. Its best role is adjudicating examples such as:

```text
رقم الحساب ١٢٣٤٥٦٧٨٩        → likely ACCOUNT_NUMBER
تم تحويل ١٢٣٤٥٦٧٨٩ جنيه     → likely AMOUNT
```

### 3. Fusion and context resolution

Start with explicit decision rules, not a learned meta-model:

1. map all detector labels into one Finaira taxonomy;
2. resolve overlapping spans using risk-aware priorities;
3. treat a valid checksum plus matching context as strong evidence;
4. combine nearby labels in Arabic and English, including RTL/LTR variants;
5. canonicalize high-confidence aliases and repeated mentions;
6. send only unresolved high-risk cases to the local SLM;
7. abstain or fail closed when uncertainty remains.

Do not average detector confidence scores. A regex score, token-classifier probability, and LLM self-reported confidence are not comparable. If enough gold data later exists, calibrate each detector per entity type and train a small interpretable fusion classifier as an experiment.

### 4. Policy engine

Detection answers “what is this?” Policy answers “what may leave?” Keep these separate.

```yaml
PERSON: tokenize
ACCOUNT_NUMBER: tokenize
IBAN: tokenize
CARD_NUMBER: tokenize
PHONE: tokenize
EMAIL: tokenize
AMOUNT: preserve
CURRENCY: preserve
LOCATION: review_or_generalize
UNRESOLVED_HIGH_RISK: block
```

Use versioned YAML/JSON plus typed validation for the MVP. A full policy platform is unnecessary until rules depend on many users, jurisdictions, purposes, and document classes.

### 5. Reversible pseudonymization and vault

Use typed, opaque placeholders such as:

```text
Ahmed Ali → [[PERSON_K7M4P9]]
OM12...   → [[IBAN_Q2X8D1]]
```

Recommended design:

- generate token IDs with a keyed construction or cryptographically random values;
- store `{token, encrypted original, type, scope, expiry, policy version}` locally;
- encrypt mapping values with authenticated encryption;
- isolate mappings by tenant and task/request;
- restore only after authorization and output validation;
- never log raw values, mapping contents, unprotected prompts, or unprotected outputs.

**Token scope is a real research trade-off:**

| Scope | Privacy | Utility |
|---|---|---|
| Per request | Minimizes linkability | Cannot reliably connect the same entity across documents |
| Per document | Supports document-level co-reference | No collection-level consistency |
| Per tenant/corpus | Supports cross-document retrieval and analysis | Reveals equality/linkability patterns to the cloud |

The project brief asks for consistency across a collection, but global stable tokens create observable links. The proposed solution is **configurable scope**, with tenant/corpus scope used only when the downstream task requires it and evaluated as a privacy–utility variable.

### 6. Cloud task and retrieval placement

Choose **one primary downstream task** for the MVP. Question answering over a small document collection is the strongest option because it exercises retrieval, context preservation, and restoration.

Recommended production-shaped flow:

1. keep raw document storage and raw indexing local;
2. retrieve the minimum required chunks locally;
3. sanitize those chunks and the user query;
4. send only sanitized top-k context to the cloud LLM;
5. require the cloud model to preserve placeholders exactly.

For the research experiment, also build a sanitized-corpus index and compare it with a raw local oracle. This isolates how pseudonymization affects retrieval without requiring raw embeddings or raw documents to leave the trusted side.

If embeddings or a vector database are hosted externally, only sanitized text and sanitized metadata may be indexed. Sanitizing only the final prompt would leave an earlier leakage path through ingestion and embeddings.

### 7. Pre-egress and post-response safety gates

Before any external call:

- scan the final payload again for raw high-risk entities;
- verify that every transformation follows the active policy;
- reject unresolved high-risk spans;
- strip unnecessary metadata and document sections.

After the cloud response:

- accept only well-formed tokens from the current mapping scope;
- never resolve an invented or cross-request token;
- rescan for unexpected raw PII;
- check whether required tokens were corrupted or dropped;
- block, retry with a stricter prompt, or request review on failure;
- restore only the tokens that the requesting user is authorized to see.

Prompt instructions are useful for preserving tokens, but they are not a security control on their own.

## Dataset strategy

Build a project-specific benchmark; do not train a large model from scratch.

Use three layers:

1. **Template-generated financial documents** with automatic span labels for scale and controlled variation.
2. **Public multilingual/Arabic resources** such as REDACT, Wojood, and AMWAL for external baselines and out-of-domain testing. [REDACT](https://github.com/guneeshvats/REDACT-PII-Benchmark) provides Arabic, code-switched cases, 51 canonical PII types, and disclosure/sensitivity slices, but it is not a substitute for Finaira-like documents.
3. **Human-reviewed Finaira-like documents**, preferably synthetic or safely de-identified templates reviewed by a domain expert. Real customer data should not be required for the university benchmark.

Required challenge slices:

- Arabic-only, English-only, and code-switched text;
- Arabic-Indic and Western digits;
- person/organization names and transliterations;
- valid and invalid/checksum-failing identifiers;
- account-number versus amount/reference ambiguity;
- adjacent and overlapping entities;
- repeated aliases and multiple people per document;
- tables, headers, footers, and optional OCR corruption;
- direct identifiers, quasi-identifiers, and contextual disclosure.

Split by document template/source, not random sentence alone, to reduce train–test leakage. Lock a human-verified test set before tuning thresholds.

## Evaluation plan

### Detection and leakage

- strict and overlap span precision, recall, and F1;
- per-type, per-language, and per-disclosure-form results;
- recall-weighted `Fβ` for high-risk entities;
- **document leakage rate:** proportion of documents where any high-risk raw entity survives;
- count and severity of leaked entities;
- false-positive removal rate, because excessive masking damages utility.

Aggregate F1 must not be the headline privacy metric. A system can score well while still leaking a rare account number or national ID.

### Reversibility and security behavior

- exact round-trip reconstruction rate;
- token collision rate;
- correct alias consistency within the selected scope;
- corrupted, missing, duplicate, and invented-token handling;
- cross-request token rejection;
- unauthorized restoration rejection;
- mapping expiry/deletion behavior;
- confirmation that telemetry contains no raw PII.

### Retrieval and cloud-task utility

For retrieval:

- Recall@k, MRR, and nDCG against a raw-text local oracle;
- performance by language and code-switch slice;
- entity-centric queries versus topic-centric queries.

For QA:

- exact match/token F1 for factual answers;
- answer correctness and evidence support;
- placeholder preservation and restoration correctness;
- abstention when the protected context is insufficient.

For summaries, use factual consistency and key-fact coverage with blinded human review on a sample. Embedding similarity can be a secondary diagnostic, not the primary utility measure.

### System performance

- median and p95 latency per stage;
- memory/compute use of each local model;
- cloud token consumption;
- throughput and failure rate by document size.

## Core experiments

| Experiment | Comparison | Decision supported |
|---|---|---|
| Detector ablation | rules; multilingual PII; Arabic NER; AMWAL; hybrid; hybrid + local SLM | Which components add measurable recall? |
| Transformation level | direct identifiers only; direct + selected quasi-identifiers; aggressive generalization | Where is the privacy–utility frontier? |
| Token representation | typed placeholder versus realistic surrogate | Is naturalness worth the extra risk/complexity? |
| Token scope | request, document, tenant/corpus | How much utility is gained for how much linkability? |
| Retrieval utility | raw local oracle versus sanitized corpus | What does protection cost in Recall@k/nDCG? |
| Contextual attack | sanitized text plus defined public/background knowledge | Can a subject still be inferred after span masking? |
| Robustness | clean text versus OCR/digit/code-switch perturbations | Where does the pipeline fail in realistic input? |

The contextual attack should be a bounded advanced experiment, not a promise of universal anonymity.

## MVP versus extensions

### MVP

- text and text-layer PDF input;
- small confirmed entity taxonomy;
- rules/checksums plus two benchmarked model families;
- local SLM only for uncertain high-risk cases;
- deterministic fusion and a versioned policy file;
- typed placeholders with one configurable scope;
- encrypted local mapping store;
- one cloud QA or summarization task;
- pre-egress scan, output validation, and authorized restoration;
- benchmark with detection, leakage, reconstruction, utility, and latency metrics.

### Defer until the vertical slice works

- training a new large NER model;
- production Kubernetes, Vault, OPA, or a full identity platform;
- every file format and sophisticated table reconstruction;
- realistic synthetic replacements as the default;
- universal legal-compliance claims;
- differential privacy, homomorphic encryption, or secure multiparty computation;
- autonomous agents;
- guarantees against all contextual re-identification.

These extensions are technically interesting but do not answer the core research question more directly than a well-evaluated hybrid gateway.

## Main risks and controls

| Risk | Consequence | Proposed control |
|---|---|---|
| Missed high-risk entity | Raw PII crosses the boundary | High-recall ensemble, second egress scan, fail closed |
| Over-masking | Retrieval/QA quality collapses | Per-type policy and privacy–utility experiments |
| OCR/offset mismatch | Wrong substring is replaced | Raw↔normalized offset map and round-trip tests |
| Stable-token linkability | Cloud correlates records | Configurable scope and per-tenant keys |
| Contextual inference | Identity remains guessable | Quasi-identifier policy and subject-level attack evaluation |
| Token corruption/invention | Incorrect restoration or data mix-up | Membership, scope, syntax, and authorization validation |
| Mapping-store compromise | Reversal of protected data | Authenticated encryption, separation, access control, expiry |
| Logs/telemetry leak | Side-channel disclosure | Metadata-only observability and automated log tests |
| Synthetic-only benchmark | Inflated performance | Human-reviewed realistic test set and hard negative cases |

## Proposed research questions

1. How much does a hybrid detector improve high-risk entity recall over rules or individual Arabic/multilingual models on Arabic–English financial text?
2. How do protection level and pseudonym scope affect retrieval and QA utility?
3. How reliably can the system preserve, validate, and restore pseudonyms through a cloud-LLM round trip?
4. Which failures remain under code-switching, numeric ambiguity, OCR noise, and contextual inference?

## Decisions required from Finaira/team

1. Which jurisdictions and financial identifiers are in scope?
2. What are the actual source formats: text PDFs, scanned PDFs, DOCX, emails, tables, or spreadsheets?
3. What is the primary cloud task: retrieval QA, summarization, extraction, translation, or classification?
4. Must the same entity remain linkable across documents, and for how long?
5. What local hardware is available?
6. Can Finaira supply document templates and domain-expert annotation review without exposing customer data?
7. What false-negative tolerance and review workflow are acceptable for each high-risk type?
8. May the team publish the benchmark schema, synthetic data, code, and evaluation results?

## Proposed decision

Adopt the hybrid pipeline above as the **working architecture for benchmarking**, with these initial constraints:

- text/text-layer PDF first;
- retrieval QA as the primary downstream task;
- rules/checksums + multilingual PII model + Arabic NER/AMWAL evidence;
- local SLM only for uncertain cases;
- typed placeholders before realistic surrogates;
- local retrieval and mapping storage;
- scoped tokens and strict egress/response validation;
- contribution centered on the benchmark and privacy–utility evaluation.

This should become a confirmed project decision only after Finaira answers the eight scope questions and the team runs a small detector/OCR feasibility benchmark.

