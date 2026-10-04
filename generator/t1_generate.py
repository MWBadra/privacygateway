"""T1 demo: fill the NBE individual account-opening form (page 1) with synthetic data.

Outputs (in generator/out_t1/):
  baseline_faker_only.json   records from plain Faker (ar_EG, ar_SA), for comparison
  records.json               records from Faker + egy-names + EgyptProvider, with gold labels
  t1_example_<n>.pdf / .png  the real NBE page 1 with the values written in
  extraction_check.json      whether each PII value survives PDF text extraction

Placement geometry lives in t1_layout.py (measured from the PDF).

Run: python t1_generate.py [--n 5] [--seed 123]
     Without --seed a fresh random seed is used and printed.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import secrets
import sys
from pathlib import Path

import pymupdf as fitz
from faker import Faker

from egypt_providers import EgyptProvider, INCOME_BANDS, to_arabic_indic
from t1_layout import CHECKBOXES, FIELDS

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent
SRC = HERE.parent / "starter_templates" / "T1_nbe_account_opening_individuals_ar.pdf"
OUT = HERE / "out_t1"
INK = (0.07, 0.19, 0.42)  # dark blue, like a pen

# PII types for gold labels (fields not listed are not personal data)
PII_TYPE = {
    "full_name_ar": "PERSON", "full_name_en": "PERSON", "cif": "CUSTOMER_ID", "printed_no": "ID_CARD_SERIAL",
    "national_id": "NATIONAL_ID", "issued_by": "LOCATION", "dob": "DATE_OF_BIRTH", "issue_date": "DATE",
    "expiry_date": "DATE", "place_of_birth": "LOCATION", "address": "ADDRESS", "mail_address": "ADDRESS",
    "home_phone": "PHONE", "mobile": "PHONE", "mobile2": "PHONE", "email": "EMAIL",
    "employer": "ORGANIZATION", "employer_address": "ADDRESS", "employer_phone": "PHONE",
    "request_no": "REFERENCE", "employment_start": "DATE",
}

# (male title, female title, work sector, education, job level)
JOB_PROFILES = [
    ("مهندس برمجيات", "مهندسة برمجيات", "قطاع خاص", "مؤهل عالي", "وظائف نمطية وتنفيذية"),
    ("محاسب", "محاسبة", "قطاع خاص", "مؤهل عالي", "وظائف نمطية وتنفيذية"),
    ("مدير مالي", "مديرة مالية", "قطاع خاص", "دراسات عليا", "إدارة عليا"),
    ("مدير مبيعات", "مديرة مبيعات", "قطاع خاص", "مؤهل عالي", "إدارة وسطى"),
    ("مندوب مبيعات", "مندوبة مبيعات", "قطاع خاص", "مؤهل متوسط", "وظائف نمطية وتنفيذية"),
    ("مصمم جرافيك", "مصممة جرافيك", "قطاع خاص", "مؤهل عالي", "وظائف نمطية وتنفيذية"),
    ("أخصائي موارد بشرية", "أخصائية موارد بشرية", "قطاع خاص", "مؤهل عالي", "إدارة وسطى"),
    ("مدرس", "مدرسة", "قطاع عام", "مؤهل عالي", "وظائف نمطية وتنفيذية"),
    ("طبيب", "طبيبة", "قطاع عام", "دراسات عليا", "وظائف نمطية وتنفيذية"),
    ("ممرض", "ممرضة", "قطاع عام", "مؤهل فوق المتوسط", "وظائف نمطية وتنفيذية"),
    ("موظف إداري", "موظفة إدارية", "قطاع عام", "مؤهل متوسط", "وظائف نمطية وتنفيذية"),
    ("مدير إدارة", "مديرة إدارة", "قطاع عام", "مؤهل عالي", "إدارة وسطى"),
    ("أستاذ جامعي", "أستاذة جامعية", "قطاع عام", "دكتوراه", "إدارة وسطى"),
    ("تاجر", "تاجرة", "اعمال حره", "مؤهل متوسط", None),
    ("محامي", "محامية", "اعمال حره", "مؤهل عالي", None),
    ("صيدلي", "صيدلانية", "اعمال حره", "مؤهل عالي", None),
    ("مقاول", "مقاولة", "اعمال حره", "مؤهل متوسط", None),
]
MARITAL = {"male": ["أعزب", "متزوج", "متزوج", "مطلق", "أرمل"],
           "female": ["آنسة", "متزوجة", "متزوجة", "مطلقة", "أرملة"]}


def baseline_faker_only(n: int, seed: int) -> list[dict]:
    """What plain Faker gives for the same fields (ar_EG names are English; ar_SA has Arabic names)."""
    out = []
    for loc in ["ar_EG", "ar_SA"]:
        f = Faker(loc)
        f.seed_instance(seed)
        for _ in range(n if loc == "ar_SA" else 1):
            out.append({
                "locale": loc, "full_name": f.name(), "address": f.address().replace("\n", ", "),
                "city": f.city(), "phone": f.phone_number(), "iban": f.iban(), "id (ssn)": f.ssn(),
                "job": f.job(), "company": f.company(), "email": f.email(),
            })
    return out


def make_record(fake: Faker, rng: random.Random, i: int) -> dict:
    gender = rng.choice(["male", "female"])
    religion = rng.choices(["muslim", "christian"], weights=[9, 1])[0]
    name_ar, name_en = fake.egyptian_name(gender, religion)
    dob = fake.date_of_birth(minimum_age=23, maximum_age=65)
    birth_gov = fake.governorate()
    home_gov = birth_gov if rng.random() < 0.6 else fake.governorate()
    issue = fake.date_between(start_date="-6y", end_date="-30d")
    district = rng.choice(home_gov["districts"])
    job_m, job_f, sector, education, level = rng.choice(JOB_PROFILES)
    start = fake.date_between(start_date=dob.replace(year=dob.year + 22), end_date="-60d")
    employer_gov = home_gov if rng.random() < 0.7 else fake.governorate()
    has_home = rng.random() < 0.5
    addr = fake.egyptian_address(home_gov)
    if sector == "اعمال حره":
        employer = ""  # self-employed: no employer name on the form
        income_source = "اعمال حره"
        band_range = (3, 10)
    else:
        employer = fake.egyptian_employer(employer_gov["ar"], public=(sector == "قطاع عام"))
        income_source = "راتب شهري"
        band_range = (2, 8) if level != "إدارة عليا" else (6, 10)
    rec = {
        "doc_id": f"T1-{i:05d}",
        "_meta": {"gender": gender, "religion": religion},
        "date": fake.date_between(start_date="-30d", end_date="today").strftime("%d/%m/%Y"),
        "request_no": f"{rng.randrange(10**6, 10**7)}",
        "branch": f"فرع {district}",
        "full_name_ar": name_ar, "full_name_en": name_en.upper() if rng.random() < 0.5 else name_en,
        "cif": fake.cif_number(), "printed_no": fake.id_card_printed_number(),
        "id_type": "بطاقة رقم قومي",
        "national_id": fake.national_id(dob, gender, birth_gov["code"]),
        "issued_by": f"سجل مدني {rng.choice(home_gov['districts'])}",
        "gender": "ذكر" if gender == "male" else "أنثى",
        "issue_date": issue.strftime("%d/%m/%Y"),
        "expiry_date": issue.replace(year=issue.year + 7).strftime("%d/%m/%Y"),
        "dob": dob.strftime("%d/%m/%Y"),
        "place_of_birth": birth_gov["ar"], "country_of_birth": "مصر",
        "nationality": "مصري" if gender == "male" else "مصرية", "other_nationality": "لا",
        "customer_type": "فرد", "disability": "لا",
        "housing": rng.choice(["إيجار", "تمليك"]),
        "address": addr, "country": "مصر",
        "mail_address": addr if rng.random() < 0.7 else fake.egyptian_address(fake.governorate()),
        "mail_country": "مصر",
        "statement_freq": rng.choice(["شهري", "ربع سنوي"]),
        "statement_lang": rng.choice(["العربية", "العربية", "الإنجليزية"]),
        "home_phone": fake.egyptian_landline(home_gov["area_code"]) if has_home else "",
        "home_cc": "+20" if has_home else "",
        "mobile": fake.egyptian_mobile(), "mobile_cc": "+20",
        "mobile2": fake.egyptian_mobile() if rng.random() < 0.3 else "",
        "email": fake.email_from_name(name_en, dob),
        "work_sector": sector,
        "profession": job_m if gender == "male" else job_f,
        "job_level": level or "",
        "employer": employer,
        "employment_start": start.strftime("%d/%m/%Y"),
        "employer_address": fake.egyptian_address(employer_gov) if employer else "",
        "employer_country": "مصر" if employer else "",
        "employer_phone": fake.egyptian_landline(employer_gov["area_code"]) if employer else "",
        "income_source": income_source,
        "income_band": INCOME_BANDS[rng.randrange(*band_range)],
        "other_banks": rng.choice(["لا", "لا", "نعم"]),
        "marital_status": rng.choice(MARITAL[gender]),
        "residence_country": "مصر",
        "residency": "مواطن مقيم",
        "education": education,
    }
    rec["mobile2_cc"] = "+20" if rec["mobile2"] else ""
    # ~40% of forms are filled with Arabic-Indic digits (checkbox values stay as keys, they are not written)
    rec["_meta"]["digits"] = "arabic" if rng.random() < 0.4 else "western"
    if rec["_meta"]["digits"] == "arabic":
        keep = {"doc_id", "email", "full_name_en", "printed_no", *CHECKBOXES}
        for k, v in rec.items():
            if isinstance(v, str) and k not in keep:
                rec[k] = to_arabic_indic(v)
    return rec


def draw_tick(page: fitz.Page, cell: tuple) -> None:
    """Hand-style X inside a checkbox cell."""
    r = fitz.Rect(cell)
    m = min(r.width, r.height) * 0.22
    inner = fitz.Rect(r.x0 + m, r.y0 + m, r.x1 - m, r.y1 - m)
    page.draw_line(inner.tl, inner.br, color=INK, width=0.9)
    page.draw_line(inner.bl, inner.tr, color=INK, width=0.9)


def fill_pdf(rec: dict, path_pdf: Path, path_png: Path) -> None:
    doc = fitz.open(SRC)
    doc.select([0])
    page = doc[0]
    arch = fitz.Archive("C:/Windows/Fonts")
    css = "@font-face {font-family: f; src: url(tahoma.ttf);} * {font-family: f; font-size: 7px; color: #12306b;}"
    for key, (x0, y0, x1, y1, direction) in FIELDS.items():
        val = rec.get(key, "")
        if not val:
            continue
        # NB: in PyMuPDF's HTML engine dir="rtl" alone right-aligns; adding text-align:right flips it left.
        html = {"rtl": f'<div dir="rtl">{val}</div>',
                "ltr": f'<div dir="ltr" style="text-align:left">{val}</div>',
                "ltr-right": f'<div style="text-align:right">{val}</div>'}[direction]
        page.insert_htmlbox(fitz.Rect(x0, y0, x1, y1), html, css=css, archive=arch)
    for field, options in CHECKBOXES.items():
        value = rec.get(field, "")
        if not value:
            continue
        if value not in options:
            raise ValueError(f"{rec['doc_id']}: no checkbox for {field}={value!r}")
        draw_tick(page, options[value])
    doc.subset_fonts()
    doc.save(path_pdf, garbage=4, deflate=True)
    page.get_pixmap(dpi=110).save(path_png)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def extraction_check(rec: dict, path_pdf: Path) -> dict:
    """Does each PII value come back verbatim from the PDF text layer?"""
    flat = norm(fitz.open(path_pdf)[0].get_text())
    res = {}
    for key, typ in PII_TYPE.items():
        val = rec.get(key, "")
        if not val:
            continue
        tokens = norm(val).split()
        res[key] = {"type": typ, "value": val, "exact_match": norm(val) in flat,
                    "tokens_found": f"{sum(t in flat for t in tokens)}/{len(tokens)}"}
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()
    seed = args.seed if args.seed is not None else secrets.randbelow(10**9)
    print(f"seed={seed}")

    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("t1_example_*"):
        old.unlink()
    (OUT / "baseline_faker_only.json").write_text(
        json.dumps(baseline_faker_only(args.n, seed), ensure_ascii=False, indent=1), encoding="utf-8")

    fake = Faker("ar_EG")
    fake.seed_instance(seed)
    fake.add_provider(EgyptProvider)
    rng = random.Random(seed)
    records, checks = [], {}
    for i in range(1, args.n + 1):
        rec = make_record(fake, rng, i)
        rec["_meta"]["seed"] = seed
        rec["gold_labels"] = [{"field": k, "type": t, "text": rec[k]} for k, t in PII_TYPE.items() if rec.get(k)]
        records.append(rec)
        pdf, png = OUT / f"t1_example_{i}.pdf", OUT / f"t1_example_{i}.png"
        fill_pdf(rec, pdf, png)
        checks[rec["doc_id"]] = extraction_check(rec, pdf)
    (OUT / "records.json").write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "extraction_check.json").write_text(json.dumps(checks, ensure_ascii=False, indent=1), encoding="utf-8")

    for rec in records:
        c = checks[rec["doc_id"]]
        ok = sum(v["exact_match"] for v in c.values())
        print(f"{rec['doc_id']}  {rec['full_name_ar']} | {rec['full_name_en']} | {rec['profession']} "
              f"| digits={rec['_meta']['digits']} | PII exact after extraction: {ok}/{len(c)}")


if __name__ == "__main__":
    main()
