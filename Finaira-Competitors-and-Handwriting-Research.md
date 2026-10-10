# Competitors and Handwritten Documents: Research Notes

Finaira Privacy Gateway project, October 2026

These notes record five questions asked during the research sessions and the answers found. Sources are listed at the end of each section.

---

## 1. Publishing the scope and legal PDFs

**Question.** Push only the two PDFs (document scope catalogue and data protection rules) to the repository.

**Answer.** Both PDFs were committed and pushed to `main`. A teammate had uploaded `Finaira_Proposal_Draft_3.pdf` in the meantime, so the local commit was rebased on top of it before pushing. Nothing was overwritten.

---

## 2. How do competitors work?

**Question.** Do competitors accept handwritten documents? Do they need to be trained on a template beforehand? What file types do they accept: PDF, images, other?

### Short answers

1. **Handwriting.** Privacy tools do not read handwriting themselves. They call a separate OCR service, and only some of those read handwriting. For Arabic handwriting, the only confirmed option is Azure Document Intelligence.
2. **Templates.** Privacy and PII tools read text and detect sensitive items by context, patterns and models. They do not need to know the form in advance. Only field extraction products need labelled examples: Azure custom models need about 5 per layout, and AWS Textract offers adapters.
3. **File types.** Plain text is always accepted. PDF, images and Office files are accepted by most, through OCR. Audio is accepted by Limina only.

### Comparison

| Product | Input accepted | Handwriting | Arabic | Needs templates? |
|---|---|---|---|---|
| Microsoft Presidio (open source) | Text. The image module accepts images and DICOM through Tesseract OCR; PDF is not mentioned. Documented as beta and "not production ready". | Not addressed | No Arabic or Egyptian ID recognizers out of the box (Egypt is not in its country list) | No |
| Private AI (now Limina) | PDF, Word, Excel, PowerPoint, CSV, JSON, XML, JPEG, PNG, TIFF, BMP, audio (WAV, MP3 and others) | Only through its Azure OCR modes, at higher cost | Arabic is "Extended" tier and **text only**: no file or audio support for Arabic | No |
| Azure AI Language (PII) | Text and documents | Not applicable | Arabic supported for text and document PII | No |
| Azure Document Intelligence (reading step) | PDF, JPEG, PNG, BMP, TIFF, HEIF, Office files | Yes, including Arabic, in version 4.0 | Printed and handwritten Arabic | Prebuilt models: no. Custom models: yes, about 5 labelled examples per layout. |
| Google Cloud Sensitive Data Protection | Images up to 4 MiB, PDF, Word, Excel, PowerPoint; OCR on images | Not stated | OCR languages not stated | No |
| AWS Textract (reading step) | JPEG, PNG, PDF, TIFF | English only | Arabic not supported | Prebuilt: no. Adapters: yes. |
| AWS Comprehend (PII) | Text | Not applicable | PII detection in English and Spanish only | No |
| AWS Bedrock Guardrails | Text | Not applicable | Arabic listed as supported | No |
| Nightfall, Protecto, Skyflow | Text and prompts; Nightfall also scans over 100 file types with OCR. Protecto and Skyflow replace values with tokens and restore them, like our gateway. | Not stated | Not stated | No. Skyflow uses a dictionary of sensitive fields that the user defines. |

The Nightfall, Protecto and Skyflow row is based on marketing pages and search summaries, not technical documentation.

### What this means for Finaira

1. Competitors do not need templates, so working on unseen printed documents is expected, not a differentiator.
2. No product covers Arabic, Egyptian identifiers, bank forms, files and handwriting together. The nearest all-in-one tool (Limina) handles Arabic as text only.
3. Handwriting is a separate component everywhere. The only Arabic handwriting reader found (Azure) is a cloud service, which conflicts with keeping data inside the organization.
4. Most competitors are cloud services. Only Presidio is fully open and local, and Limina offers a container for on-premises use.

No published accuracy figures were found for Arabic handwriting on Egyptian forms.

### Sources

- [Azure Document Intelligence, language support for Read and Layout](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/language-support/ocr?view=doc-intel-4.0.0)
- [Azure Document Intelligence, custom models](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/train/custom-model)
- [Azure AI Language, PII language support](https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/language-support)
- [AWS Textract quotas and languages](https://docs.aws.amazon.com/textract/latest/dg/limits-document.html)
- [AWS Comprehend PII](https://docs.aws.amazon.com/comprehend/latest/dg/pii.html)
- [AWS Bedrock Guardrails languages](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-supported-languages.html)
- [Google Sensitive Data Protection, supported file types](https://docs.cloud.google.com/sensitive-data-protection/docs/supported-file-types)
- [Presidio image redactor](https://presidio.dataprivacystack.org/image-redactor/)
- [Presidio supported entities](https://presidio.dataprivacystack.org/supported_entities/)
- [Limina supported file types](https://docs.getlimina.ai/configuration-and-operations/working-with-files/supported-file-types.md)
- [Limina OCR modes](https://docs.getlimina.ai/configuration-and-operations/working-with-files/processing-files/ocr-modes.md)
- [Limina languages](https://docs.getlimina.ai/languages.md)
- [Nightfall](https://www.nightfall.ai/lp/cloud-dlp), [Protecto](https://www.protecto.ai/solutions/llm-data-privacy-security-dlp/), [Skyflow](https://www.skyflow.com/post/generative-ai-data-privacy-skyflow-llm-privacy-vault)

---

## 3. Proposal: handle handwriting by cropping it instead of reading it

**Question.** Normal printed PDFs can be processed without a template. But many real documents are partly handwritten, and the handwritten parts sit in known places on the form, defined by printed labels. Proposal: use a template only for handwritten documents. Locate each handwritten field, cut it out, replace it with an ID, send the rest to the cloud model, and put the original crop back when the answer returns. Arabic handwriting recognition, which is very hard and unreliable, is never needed. An extra layer would analyse each template once, save the field locations, and record which fields must be blocked. How does this compare with research and competitors?

### Verdict

The idea is sound. No product or paper doing exactly this was found. The building blocks exist separately, so the combination is a credible contribution.

### Comparison with existing approaches

| Approach | Who does it | Reads handwriting? | Reversible? | Needs a template? | Main weakness |
|---|---|---|---|---|---|
| Full handwriting recognition, then PII detection | Azure Document Intelligence with Azure PII; Limina with Azure OCR | Yes | Partly (Limina) | No | Arabic handwriting recognition is error prone; cloud only |
| Zonal OCR and ICR on fixed forms | ABBYY FlexiCapture, zonal OCR products | Yes, but ICR reads only separated hand printed characters, not cursive | No | Yes | Built to read fields, not to protect them |
| Fixed zone redaction | Laserfiche Fixed Annotation, Hyland OnBase, Tungsten (Kofax) redaction modules | No | No, permanent | Yes | One way; no LLM use; fields have no meaning attached |
| Fixed region masking in medical images | DICOM anonymisers (RSNA CTP, Orthanc Pixels Masker, XNAT) | No | No | Yes, per scanner model | Shows that position based masking is accepted in a regulated field |
| Custom form models | Azure custom template models (about 5 labelled samples per layout, layout must stay the same) | Yes | No | Yes | Same "one model per layout" burden |
| **Finaira proposal** | Not found elsewhere | **No** | **Yes** | Yes, with a fallback without one | The cloud model never sees the handwritten value |

### Why the idea is strong

1. **Reading errors cannot cause leaks.** In OCR first pipelines, a misread name can escape the PII detector. Hamdi and colleagues measured how OCR errors reduce named entity recognition accuracy. Masking the whole zone fails safe.
2. **It avoids the hardest problem.** On the KHATT Arabic handwriting benchmark, recent 2024 models report 13 to 18 percent character error; some papers claim about 3 percent. All are clean laboratory text lines.
3. **It is cheap and local.** Alignment and cropping need no GPU and no cloud service.
4. **Template work happens once per form**, not per document.

### Problems to design for

1. **The model only sees a placeholder** such as `[NAME_1]`. Tasks that need the value fail, for example checking that an amount in digits matches the amount in words. A restored answer that mixes text and image crops works in a viewer, not in a database field.
2. **Handwriting outside known zones**: margin notes, corrections, overflow, names written in remarks. Fix: subtract the aligned blank form from the filled page and mask any leftover ink.
3. **Tick boxes are sensitive** (income band, disability, political exposure). Mask them, or read their state locally, which is easy.
4. **Alignment**: skewed scans, phone photos, page order, and new form versions (the downloaded bank forms carry version codes). Identify the form and version, align it with feature matching and a homography, and fall back below a confidence threshold.
5. **Stamps and signatures** often cover printed text and should be zones too.
6. **Template library growth.** Form field detectors trained on CommonForms (2025, about 450,000 pages) can propose field boxes on a blank form. The template analysis layer can attach a meaning to each field from its nearby label (for example الاسم بالكامل becomes NAME), and a person confirms once.

### Improvement: three tiers

| Tier | When | What happens |
|---|---|---|
| A. Mask and pass through | Known form; names, addresses, free text | The original proposal |
| B. Constrained local reading | Known form; digit boxes and tick boxes | Read single digits only, then validate with known structures such as the national ID format. Isolated Arabic handwritten digits reach about 99 percent on MADBase. The model receives facts like "valid ID", never the value. |
| C. No template | Unknown form or failed alignment | A handwriting detector separates handwriting from print (for example HTSNet) and **all** handwriting is masked |

```
page -> identify form -> known? -yes-> align -> zones -> tier A or B per field --+
                      -no--> handwriting detector -> mask all handwriting (C) ---+
printed text -> normal text pipeline (detect, pseudonymise) -------------------+
leftover ink check (filled page minus blank form) -> mask anything unexpected -+
                                 v
                 cloud model -> answer -> restore tokens and image crops locally
```

### Research framing

Reversible, recognition free masking of handwritten fields before a cloud language model. It can be evaluated against a full recognition baseline (Azure Arabic handwriting) on four measures:

- leak rate
- alignment success
- task usefulness
- cost and latency

The MADBase and KHATT figures come from clean benchmarks. Real forms will perform worse.

### Sources

- [Azure custom models](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/train/custom-model)
- [ABBYY handwriting recognition properties](https://docs.abbyy.com/flexi-capture/templates/properties-recognition-text-htr)
- [Reading handprint and checkmarks with FlexiCapture](https://www.simpleocr.com/knowledge-base/reading-handprint-checkmarks-and-forms-with-flexicapture-and-vantage/)
- [Laserfiche Fixed Annotation](https://doc.laserfiche.com/laserfiche/en-us/content/capture-qf-fixed-annotation.htm)
- [Hyland OnBase Automated Redaction](https://support.hyland.com/r/OnBase/Automated-Redaction/English/Foundation-22.1/Automated-Redaction/Configuration/Automated-Redaction-and-Advanced-Capture/Overview)
- [Tungsten redaction modules](https://marketplace.tungstenautomation.com/details/redaction-modules)
- [Zonal OCR](https://www.llamaindex.ai/glossary/zonal-ocr)
- [RSNA CTP](https://rsna.org/ctp.aspx)
- [Orthanc Pixels Masker](https://orthanc.uclouvain.be/book/plugins/pixels-masker.html)
- [XNAT pixel anonymization](https://wiki.xnat.org/xnat-tools/applying-pixel-anonymization-during-the-upload-pro)
- [Hamdi et al., OCR errors and NER](https://cambridge.org/core/journals/natural-language-engineering/article/indepth-analysis-of-the-impact-of-ocr-errors-on-named-entity-recognition-and-linking/C732399FF72BAFE8FF830BB1F5ED7576)
- [KHATT model](https://www.researchgate.net/publication/381429976_An_End-to-End_Segmentation-Free_Arabic_Handwritten_Recognition_Model_on_KHATT)
- [Arabic handwriting review](https://www.researchgate.net/publication/403566830_Handwritten_Arabic_Text_Recognition_A_Review_of_Recent_Trends_and_Future_Direction)
- [MADBase results](https://ijeecs.iaescore.com/index.php/IJEECS/article/view/21860)
- [HTSNet](https://arxiv.org/abs/1906.05229)
- [Zagoris et al. 2012](https://www.primaresearch.org/www/assets/papers/ICFHR2012_Zagoris_TextSeparation.pdf)
- [CommonForms](https://arxiv.org/abs/2509.16506v1)
- [FUNSD](https://arxiv.org/pdf/1905.13538)
- [Feature based alignment](https://learnopencv.com/image-alignment-feature-based-using-opencv-c-python/)

---

## 4. Which handwritten data is usable, and which must stay blocked?

**Question.** Since some handwritten entities may be useful but get blocked by the cropping approach, which document types in the scope catalogue contain handwriting, and which of that handwritten data is not very sensitive under the rules list?

### Short answer

Most handwritten content is P0 or P1 and must stay blocked. The usable part is mostly **tick boxes and closed choices**, not cursive text, and ticks are easy to read locally.

### By document type

| Document type | Handwriting | Blocked handwritten fields (P0 and P1) | Usable handwritten fields |
|---|---|---|---|
| Account opening and KYC forms | Mostly handwritten | Names (Arabic and Latin), national ID, CIF, address, phones, email, birth date and place, ID dates, employer and job, joint holders, signature. Tick boxes that stay P0: income band and income sources (financial data), disability (health), account purpose and expected activity (Law 194). | P2 ticks: gender, nationality, marital status, education, housing, residency, customer type. Keep ticks: statement frequency, method and language, account type, currency. Employment type tick: P1, allowed in general form. |
| Loan agreements and applications | Partly (blanks, signature on every page) | Borrower name, ID, address, amounts in digits and words, loan account and certificate numbers, guarantors, collateral, staff names | Loan purpose ticks and instalment frequency (borderline under Law 194), blank filled or not, page signed or not |
| Transfer forms (paper) | Mostly handwritten | Accounts, IBAN, beneficiary name, address and bank, amount, purpose, signatory | Transfer type, charges option, currency tick (currency is borderline) |
| Card, dispute and service forms | Mostly handwritten | Card and account numbers, contact details, transaction table, free text description | Dispute reason ticks, description present or not |
| Terms and conditions | Name, date and signature only | Name, signature | Signed or not, dated or not |
| Bank statements (certified) | Stamp and signature only | Employee signature | Stamped or not, signed or not |
| National ID copies | "True copy" note and signature | Signature | Note present or not |
| Salary certificates | Signature, sometimes the whole letter | Name, ID, salary figures (P0); employer and job (P1) | Stamp and signature present or not |
| Commercial register and tax cards | Stamps, older handwritten notes | Partner names and dates | Stamp present or not |
| Complaints (branch letters) | Fully handwritten | Everything (free text mixing names, numbers, amounts) | Letter present, length |
| Trade finance, financial reports | Signature only | Signatures | Signed or not |
| Insurance claims (not included) | Mostly handwritten | Health data, all of it | Not applicable |

### Three groups

1. **Read locally and send the value**: P2 and Keep ticks (gender, nationality, marital status, education, housing, residency, customer type, statement settings, account type, currency, transfer type, charges option, dispute reason). P2 is allowed because the surrounding identifiers are masked.
2. **Read locally and send a general form**: P1 fields. Birth date becomes an age band, ID expiry becomes valid or expired, employment tick becomes sector, job title becomes occupation category, start date becomes years in job, and the politically exposed tick becomes yes or no if policy allows. Limit how many general facts leave per document, because together they can narrow down a person.
3. **Never sent; only "present or not"**: names, ID numbers, phones, addresses, account numbers, amounts, signatures, income and disability ticks, and everything on minors' forms. Completeness flags reveal nothing and support the most common task on forms: checking whether they are complete.

### Design consequences

- Each template zone gets one of four modes: read value, read as general fact, presence only, mask only.
- The largest utility loss is free text (dispute descriptions, handwritten complaints). It is P0 throughout and has no safe partial form without a reliable local reader.
- Two decisions for the client's compliance team:
  - Are loan term ticks and transfer currency "transaction details" under Law 194 Article 140?
  - Should the armed forces and police employment options be treated as more sensitive?

---

## 5. Usable handwritten fields, and research on cropping and restoring

**Question.** List the handwritten information at P2 or less sensitive that needs to be understood, describe how it looks, and find papers and projects that crop parts of a document and put them back.

### 5.1 Handwritten information to understand

#### A. Read and send the value (P2 and Keep)

| Information | Priority | Where | How it looks | How to read locally |
|---|---|---|---|---|
| Gender | P2 | KYC forms | Two ticks (ذكر / أنثى) or a word on a dotted line | Tick state, or two possible words. Also contained in the national ID (13th digit) if read locally. |
| Nationality, other nationalities | P2 | KYC forms | A word on a line (مصري), sometimes an "Egyptian / other" tick | Tick, or a fixed list of countries |
| Marital status | P2 | KYC forms and updates | Three or four ticks (أعزب، متزوج، مطلق، أرمل) | Tick |
| Education | P2 | KYC forms | Four or five ticks (أمي، مؤهل متوسط، عالي، دراسات عليا) | Tick |
| Housing type | P2 | KYC forms | Ticks (ملك، إيجار، أخرى) | Tick |
| Residency status | P2 | KYC forms | Ticks (مقيم / غير مقيم) | Tick |
| Customer type | P2 | KYC forms | Ticks | Tick |
| Branch name | P2 | Most bank forms | A word on a line at the top | Match against the bank's branch list. Keep the request number masked: branch, request number and date together point to one record. |
| Statement frequency, method, language | Keep | Account opening | Ticks | Tick |
| Account type, account currency | Keep | Account opening, deposit forms | Ticks | Tick |
| Transfer type | Keep | Paper transfer forms | Ticks (internal, wire, manager's cheque) | Tick |
| Charges option | Keep | Transfer forms | Three ticks (sender, beneficiary, shared) | Tick |
| Dispute reason | Keep | Card dispute forms | A column of 8 to 10 printed reasons with ticks | Tick |
| Card type requested | Keep | Card applications | Ticks | Tick |
| Filled or empty, signed or not, stamped or not, thumbprint present | Keep (derived) | Every form | Ink in a zone; a signature line; a round or rectangular stamp | Ink count per zone, no reading needed |

#### B. Read but send only in a general form (P1)

| Information | How it looks | Read locally as | Send |
|---|---|---|---|
| Date of birth | Digits in 6 to 8 boxes, or three blanks for day, month and year | Single digits | Age band |
| ID expiry date | Digits in boxes | Single digits | Valid or expired |
| Employment type | Ticks (قطاع عام، قطاع خاص، أعمال حرة، طالب، بالمعاش، لا يعمل، قوات مسلحة، شرطة) | Tick | Sector. Armed forces and police need a compliance decision. |
| Job title | Free words on a line | Hard (free handwriting) | Occupation category, only if read reliably; otherwise masked |
| Employment start date | Digits | Single digits | Years in job band |
| Politically exposed person | Yes or no tick | Tick | Yes or no, if policy allows |
| Place of birth | A word on a line | Governorate and country list | Country, or Egypt only |

#### C. Borderline (compliance decision)

Loan purpose ticks, instalment frequency ticks, and the currency on a transfer. These may count as transaction or loan details under Law 194 Article 140.

**Key point.** Almost everything usable is a tick box or a single digit in a box. None of it needs Arabic handwriting recognition, and free handwriting is almost all P0 or P1 anyway. This supports the crop and restore design.

### 5.2 Papers and projects on cropping and restoring

No single work combines all four steps: cropping by layout, a typed placeholder, a cloud model round trip, and pasting the crop back. Each half exists.

#### Cropping fields from forms with a known layout

| Work | What it does | Relevance |
|---|---|---|
| **ODK Scan / ODK-X Scan** (University of Washington, open source) | A JSON template stores each field's location. Bubbles, checkboxes and written numbers are read automatically, and image snippets of handwritten text are saved for manual entry. | Closest match to tiers A and B |
| **Dell, Breit, Wobbrock, Borriello. "Improving Form-Based Data Entry with Image Snippets." Graphics Interface 2013** | Segments a form image into one snippet per field. Data entry was 28.3 percent faster on desktop with no detectable loss of accuracy. | Academic evidence for field cropping |
| **Shreddr** (Chen, Kannan, Yano, Hellerstein, Parikh. ACM DEV 2012; later Captricity) | Cuts forms into field images for crowd workers. Over one million values were entered from 36,819 pages in Mali. | Same cropping at scale; workers see only pieces out of context |
| **Snippet keying in commercial capture** (IBM Datacap; ScaleHub snippeting; patent US 2015/0213283) | Operators see only one field's crop, never the full page, explicitly for privacy | Direct precedent for cropping as protection |

#### Masking fixed regions (no restore)

| Work | What it does |
|---|---|
| Laserfiche Fixed Annotation, Hyland OnBase, Tungsten (Kofax) redaction | Black out the same zone on every copy of a known form |
| DICOM pixel anonymisers (RSNA CTP, Orthanc Pixels Masker, XNAT) | Black out fixed rectangles per scanner type |

#### Placeholder and restore for text

| Work | What it does |
|---|---|
| HaS (Hide and Seek, 2023) and Portcullis (AAAI) | Hide sensitive text before a cloud model and restore it afterwards |
| Microsoft Presidio anonymize and deanonymize | Reversible operators that restore original values in the response |
| LLM Guard (Protect AI) | The Anonymize scanner stores originals in a vault; the Deanonymize scanner restores them |
| LangChain reversible anonymizer, Skyflow and Protecto vaults | The same token and restore pattern as products |

#### Reversible protection inside the image

| Work | What it does | Why Finaira does not need it |
|---|---|---|
| Gu et al., "Password-conditioned Anonymization and Deanonymization with Face Identity Transformers", ECCV 2020 | Replaces faces; the right password restores them | The crop never leaves the organization, so no cryptographic restore is needed |
| Reversible data hiding in encrypted images | Encrypts regions and restores them with a key | Same reason |
| CloakDiff (ACM MM 2026) | Reversible image protection against vision language models | Same reason |

#### Risk to cite

**Lopresti and Spitz, "Information Leakage Through Document Redaction: Attacks and Countermeasures", SPIE 2005.** Redacted text was recovered from the size of the black box and leftover letter traces. Consequences for Finaira:

- placeholders must not reveal crop size or length;
- zones should be expanded slightly so no stray ink remains;
- a leftover ink check is needed.

#### The gap

ODK Scan and Shreddr crop by layout but send crops to people. Presidio, HaS and Portcullis restore placeholders but work on text only. No work was found that crops handwritten fields by layout, replaces them with typed placeholders, sends the document to a cloud language model, and pastes the crops back into the answer.

The "how it looks" column is based on the public blank bank forms collected (NBE, Banque Misr, HSBC) and on typical practice, not on filled real world copies.

### Sources

- [ODK-X Scan](https://docs.odk-x.org/scan-intro/)
- [ODK Scan user guide](https://odk-x.org/assets/wp-content/uploads/2013/05/ODK-Scan-User-Guide.pdf)
- [Dell et al., GI 2013](https://faculty.washington.edu/wobbrock/pubs/gi-13.01.pdf)
- [Shreddr, ACM DEV 2012](https://dsf.berkeley.edu/papers/dev12-shreddr.pdf)
- [ScaleHub snippeting](https://scalehub.com/snippeting-the-key-to-efficient-secure-crowdsourcing/)
- [IBM Datacap](https://www.ibm.com/docs/en/SSZRWV_9.1.4/com.ibm.dc.reference.doc/dcaca793.htm)
- [Patent US 2015/0213283](https://patents.justia.com/patent/20150213283)
- [Laserfiche Fixed Annotation](https://doc.laserfiche.com/laserfiche/en-us/content/capture-qf-fixed-annotation.htm)
- [Hyland OnBase](https://support.hyland.com/r/OnBase/Automated-Redaction/English/Foundation-22.1/Automated-Redaction/Configuration/Automated-Redaction-and-Advanced-Capture/Overview)
- [Tungsten redaction](https://marketplace.tungstenautomation.com/details/redaction-modules)
- [Orthanc Pixels Masker](https://orthanc.uclouvain.be/book/plugins/pixels-masker.html)
- [XNAT pixel anonymization](https://wiki.xnat.org/xnat-tools/applying-pixel-anonymization-during-the-upload-pro)
- [RSNA CTP](https://rsna.org/ctp.aspx)
- [HaS](https://arxiv.org/abs/2309.03057)
- [Portcullis](https://ojs.aaai.org/index.php/AAAI/article/view/32088)
- [Presidio deanonymize](https://unpkg.com/presidio-anonymizer-nestjs@0.0.12/README.md)
- [LLM Guard example](https://huggingface.co/spaces/retereum/student-llm-guard/blob/main/LLM/LLMGuard/GuardProcessor.py)
- [LangChain data anonymizer](https://git.blob42.xyz/Archives/langchain/commits/commit/0f81b3dd2f8fa73bb9379988a270f87ba1135d6b/libs/experimental/langchain_experimental/data_anonymizer)
- [Gu et al., ECCV 2020](https://www.ecva.net/papers/eccv_2020/papers_ECCV/html/4416_ECCV_2020_paper.php)
- [Reversible data hiding in encrypted images](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9317712/)
- [CloakDiff](https://arxiv.org/abs/2607.10329)
- [Lopresti and Spitz, SPIE 2005](https://www.cse.lehigh.edu/~lopresti/Publications/2005/spie05a.pdf)
