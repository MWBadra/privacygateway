"""Faker providers for Egyptian banking PII.

Faker's own ar_EG locale only localizes dates; names, addresses, phones,
IBANs and IDs all fall back to en_US. This module fills those gaps.
Names come from the egy-names package (faker-egy-names); everything else
is rule-based and kept internally consistent (ID <-> birth date, gender,
governorate; landline <-> governorate; email <-> English name).

Assumptions that are NOT verified against an official source are marked
ASSUMPTION and must be checked before any claim about format validity.
"""

from __future__ import annotations

import datetime as dt
import random

import egy_names
from faker.providers import BaseProvider

# code (as used in the national ID), Arabic, English, landline area code,
# population weight (rough), districts (Arabic)
GOVERNORATES = [
    ("01", "القاهرة", "Cairo", "02", 10, ["مدينة نصر", "مصر الجديدة", "المعادي", "شبرا", "حلوان", "الزيتون", "عين شمس", "المقطم"]),
    ("02", "الإسكندرية", "Alexandria", "03", 6, ["سموحة", "سيدي جابر", "المنتزه", "العجمي", "محرم بك", "ميامي"]),
    ("03", "بورسعيد", "Port Said", "066", 1, ["حي الشرق", "حي العرب", "بورفؤاد"]),
    ("04", "السويس", "Suez", "062", 1, ["الأربعين", "فيصل", "عتاقة"]),
    ("11", "دمياط", "Damietta", "057", 1, ["دمياط الجديدة", "فارسكور", "رأس البر"]),
    ("12", "الدقهلية", "Dakahlia", "050", 5, ["المنصورة", "طلخا", "ميت غمر", "السنبلاوين"]),
    ("13", "الشرقية", "Sharqia", "055", 5, ["الزقازيق", "بلبيس", "العاشر من رمضان", "منيا القمح"]),
    ("14", "القليوبية", "Qalyubia", "013", 4, ["بنها", "شبرا الخيمة", "قليوب", "الخانكة"]),
    ("15", "كفر الشيخ", "Kafr El Sheikh", "047", 2, ["كفر الشيخ", "دسوق", "بيلا"]),
    ("16", "الغربية", "Gharbia", "040", 4, ["طنطا", "المحلة الكبرى", "كفر الزيات", "زفتى"]),
    ("17", "المنوفية", "Monufia", "048", 3, ["شبين الكوم", "منوف", "مدينة السادات", "أشمون"]),
    ("18", "البحيرة", "Beheira", "045", 4, ["دمنهور", "كفر الدوار", "رشيد", "إيتاي البارود"]),
    ("19", "الإسماعيلية", "Ismailia", "064", 1, ["الإسماعيلية", "فايد", "القنطرة"]),
    ("21", "الجيزة", "Giza", "02", 9, ["الدقي", "المهندسين", "الهرم", "فيصل", "السادس من أكتوبر", "الشيخ زايد", "العجوزة"]),
    ("22", "بني سويف", "Beni Suef", "082", 2, ["بني سويف", "الواسطى", "ببا"]),
    ("23", "الفيوم", "Fayoum", "084", 2, ["الفيوم", "سنورس", "طامية"]),
    ("24", "المنيا", "Minya", "086", 4, ["المنيا", "ملوي", "سمالوط", "بني مزار"]),
    ("25", "أسيوط", "Assiut", "088", 3, ["أسيوط", "ديروط", "منفلوط"]),
    ("26", "سوهاج", "Sohag", "093", 4, ["سوهاج", "جرجا", "أخميم", "طهطا"]),
    ("27", "قنا", "Qena", "096", 3, ["قنا", "نجع حمادي", "قوص"]),
    ("28", "أسوان", "Aswan", "097", 1, ["أسوان", "كوم أمبو", "إدفو"]),
    ("29", "الأقصر", "Luxor", "095", 1, ["الأقصر", "إسنا", "أرمنت"]),
    ("31", "البحر الأحمر", "Red Sea", "065", 1, ["الغردقة", "سفاجا", "القصير"]),
    ("32", "الوادي الجديد", "New Valley", "092", 1, ["الخارجة", "الداخلة"]),
    ("33", "مطروح", "Matrouh", "046", 1, ["مرسى مطروح", "الضبعة"]),
    ("34", "شمال سيناء", "North Sinai", "068", 1, ["العريش", "بئر العبد"]),
    ("35", "جنوب سيناء", "South Sinai", "069", 1, ["شرم الشيخ", "الطور", "دهب"]),
]

STREETS = [
    "شارع التحرير", "شارع الجمهورية", "شارع 26 يوليو", "شارع جمال عبد الناصر",
    "شارع سعد زغلول", "شارع النصر", "شارع الجلاء", "شارع المحطة", "شارع الثورة",
    "شارع مصطفى النحاس", "شارع عباس العقاد", "شارع الهرم", "شارع البحر",
    "شارع بورسعيد", "شارع طلعت حرب", "شارع الشهيد أحمد حمدي", "شارع المدارس",
    "شارع الجيش", "شارع الإمام علي", "شارع عمر بن الخطاب", "شارع الصفا والمروة",
]

# (male, female) job titles; Arabic gender agreement matters for the form
JOBS = [
    ("مهندس برمجيات", "مهندسة برمجيات"), ("محاسب", "محاسبة"), ("طبيب", "طبيبة"),
    ("مدرس", "مدرسة"), ("صيدلي", "صيدلانية"), ("مهندس مدني", "مهندسة مدنية"),
    ("موظف بنك", "موظفة بنك"), ("مدير مبيعات", "مديرة مبيعات"), ("ممرض", "ممرضة"),
    ("محامي", "محامية"), ("أخصائي موارد بشرية", "أخصائية موارد بشرية"),
    ("فني كهرباء", "فنية معمل"), ("تاجر", "تاجرة"), ("موظف إداري", "موظفة إدارية"),
    ("مندوب مبيعات", "مندوبة مبيعات"), ("مصمم جرافيك", "مصممة جرافيك"),
]

PUBLIC_EMPLOYERS = [
    "وزارة التربية والتعليم", "الهيئة القومية للبريد", "وزارة الصحة والسكان",
    "مصلحة الضرائب المصرية", "الشركة القابضة لمياه الشرب والصرف الصحي",
    "هيئة السكك الحديد", "جامعة {city}",
]
_CO_PREFIX = ["شركة", "مؤسسة", "مجموعة", "مصنع"]
_CO_NAME = ["النيل", "الدلتا", "الأهرام", "مصر", "القاهرة", "الصعيد", "النور", "الفجر", "السلام", "الرواد", "المستقبل"]
_CO_ACTIVITY = ["للمقاولات", "للتجارة والتوزيع", "للصناعات الغذائية", "للبرمجيات", "للأدوية",
                "للاستيراد والتصدير", "للنقل والخدمات اللوجستية", "للاستشارات الهندسية", "للملابس الجاهزة"]
_CO_SUFFIX = ["ش.م.م", "ش.م.م.", "ذ.م.م", ""]

MOBILE_PREFIXES = ["010", "011", "012", "015"]
EMAIL_DOMAINS = ["gmail.com", "gmail.com", "gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]

INCOME_BANDS = [  # matches the 15 options printed on the NBE form
    "أقل من 5 الف جم", "5 الف جم وأقل من 10 الف جم", "10 الف جم وأقل من 20 الف جم",
    "20 الف جم وأقل من 30 الف جم", "30 الف جم وأقل من 70 الف جم", "70 الف جم وأقل من 100 الف جم",
    "100 الف جم وأقل من 200 الف جم", "200 الف جم وأقل من 300 الف جم", "300 الف جم وأقل من 400 الف جم",
    "400 الف جم وأقل من مليون جم", "أكثر من مليون جم",
]

AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def to_arabic_indic(s: str) -> str:
    return s.translate(AR_DIGITS)


class EgyptProvider(BaseProvider):
    """Egyptian identity, contact and employment data."""

    def governorate(self):
        g = self.generator.random.choices(GOVERNORATES, weights=[x[4] for x in GOVERNORATES])[0]
        return {"code": g[0], "ar": g[1], "en": g[2], "area_code": g[3], "districts": g[5]}

    def egyptian_name(self, gender: str, religion: str | None = None):
        """(arabic, english) full patronymic name, 4-5 parts."""
        n = egy_names.generate_names(count=1, gender=gender, religion=religion,
                                     seed=self.generator.random.randrange(1 << 30))[0]
        return n.ar, n.en

    def national_id(self, dob: dt.date, gender: str, gov_code: str) -> str:
        """14 digits: century, YYMMDD, governorate, 3-digit serial, gender digit, check digit.

        Gender digit: odd = male, even = female.
        ASSUMPTION: the 14th check digit algorithm is not publicly documented by an
        official source we found; it is random here. Do not treat these as 'valid'.
        """
        r = self.generator.random
        century = "2" if dob.year < 2000 else "3"
        serial = f"{r.randrange(1000):03d}"
        gdigit = r.choice("13579" if gender == "male" else "02468")
        return f"{century}{dob:%y%m%d}{gov_code}{serial}{gdigit}{r.randrange(10)}"

    def egyptian_mobile(self) -> str:
        r = self.generator.random
        return r.choice(MOBILE_PREFIXES) + f"{r.randrange(10**8):08d}"

    def egyptian_landline(self, area_code: str) -> str:
        r = self.generator.random
        n = 8 if area_code == "02" else 7
        return area_code + f"{r.randrange(10**n):0{n}d}"

    def egyptian_address(self, gov: dict) -> str:
        r = self.generator.random
        parts = [f"{r.randint(1, 180)} {r.choice(STREETS)}"]
        if r.random() < 0.5:
            parts.append(f"الدور {r.randint(1, 12)} شقة {r.randint(1, 40)}")
        parts += [r.choice(gov["districts"]), gov["ar"]]
        return "، ".join(parts)

    def egyptian_employer(self, city: str, public: bool | None = None) -> str:
        """Public-sector body or a fictional private company.
        public=None picks at random (35% public)."""
        r = self.generator.random
        if public is None:
            public = r.random() < 0.35
        if public:
            return r.choice(PUBLIC_EMPLOYERS).format(city=city)
        name = f"{r.choice(_CO_PREFIX)} {r.choice(_CO_NAME)} {r.choice(_CO_ACTIVITY)}"
        suffix = r.choice(_CO_SUFFIX)
        return f"{name} {suffix}".strip()

    def egyptian_job(self, gender: str) -> str:
        m, f = self.generator.random.choice(JOBS)
        return m if gender == "male" else f

    def email_from_name(self, name_en: str, dob: dt.date) -> str:
        r = self.generator.random
        toks = name_en.lower().replace("-", "").split()
        first, last = toks[0], toks[-1]
        style = r.choice([f"{first}.{last}", f"{first}{last}", f"{first}_{last}{dob:%y}",
                          f"{first}.{toks[1]}{r.randint(1, 99)}", f"{first}{dob.year}"])
        return f"{style}@{r.choice(EMAIL_DOMAINS)}"

    def cif_number(self) -> str:
        """ASSUMPTION: NBE CIF format is not public; 9 random digits."""
        return f"{self.generator.random.randrange(10**8, 10**9)}"

    def id_card_printed_number(self) -> str:
        """ASSUMPTION: format of the factory number on the back of the ID card is not
        verified; 2 Latin letters + 7 digits."""
        r = self.generator.random
        return "".join(r.choice("ABCDEFGHJKLMNPRSTUVWXYZ") for _ in range(2)) + f"{r.randrange(10**7):07d}"
