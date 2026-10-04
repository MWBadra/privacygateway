# Privacy Gateway (Finaira graduation project)

Local, policy-driven privacy gateway for Arabic-English financial documents: detect sensitive data,
replace it with reversible placeholders, send only the protected text to a cloud LLM, and restore it locally.

## Contents
| Path | What |
|---|---|
| `Finaira-Privacy-Gateway-Proposed-Pipeline-and-Evaluation-2026-10-01.md` | Proposed pipeline and evaluation plan |
| `Finaira GP Sponsorship Deck Sept 2026.pptx` | Sponsorship proposal deck |
| `Finaira_Research_Topics_Student_Brief.pdf` | Sponsor brief (our topic: Topic 2, Privacy) |
| `templates/` | Public blank documents from Egyptian banks, by category (see its README) |
| `banque_misr/` | Banque Misr documents (Egypt + UAE branch) with a scan report |
| `starter_templates/` | The 3 Arabic-focused templates chosen to start dataset generation |
| `generator/` | Synthetic data generator (T1: NBE account-opening form) |

## Generator quick start
```
pip install faker faker-egy-names pymupdf
python generator/t1_generate.py --n 5          # new random seed each run
python generator/t1_generate.py --seed 244818072  # reproduce a run
```
Outputs go to `generator/out_t1/`: filled PDFs and PNGs, `records.json` (values + gold labels),
and `extraction_check.json` (which values survive PDF text extraction).

## Note on the bank documents
All bank PDFs are public, blank documents downloaded from the banks' own websites. They contain no
customer data. They are kept here for layout and field-structure study only and remain the property
of their respective banks.
