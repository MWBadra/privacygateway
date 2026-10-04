"""Measured layout of NBE account-opening form, page 1 (595 x 842 pt).

Every box below was derived from the PDF itself, not guessed:
  - label positions: character-level ink boxes (page.get_text("rawdict")),
    because line boxes include padding spaces and are too wide;
  - checkboxes: cells reconstructed from the thin filled rectangles the form
    uses as table borders (page.get_drawings());
  - underlines: the long thin horizontal rectangles under some left-hand fields.
Debug overlays of this geometry are in generator/debug/grid_*.png.

The form is right-to-left. A value goes in the blank space to the LEFT of its
label, right-aligned against the label. A checkbox sits to the RIGHT of its
option text.
"""

# field -> (x0, y0, x1, y1, direction). direction: "rtl" (right-aligned), "ltr" (left-aligned)
FIELDS = {
    # header
    "date":             (20, 15, 112, 24, "rtl"),       # label التاريخ: ink 115-135
    "request_no":       (290, 38, 383, 50, "rtl"),      # label رقم الطلب: ink 386-425
    "branch":           (430, 38, 546, 50, "rtl"),      # label الفرع: ink 549-574
    # section 1 - basic data
    "full_name_ar":     (300, 81, 534, 91, "rtl"),      # label الاسم بالكامل: ink 537-577
    "full_name_en":     (93, 81, 296, 91, "ltr"),       # right of "English Name" ink 29-89
    "cif":              (215, 92, 536, 102, "rtl"),     # label رقم الـCIF: ink 539-577
    "printed_no":       (18, 92, 137, 101.5, "rtl"),    # on underline 15.7-137.3 @ y101.8
    "id_type":          (405, 103, 541, 113, "rtl"),    # label نوع الهوية: ink 544-577
    "national_id":      (205, 103, 365, 113, "rtl"),    # label رقم الهوية: ink 368-399
    "issued_by":        (30, 103, 146, 112.5, "rtl"),   # on underline 29.3-146.3 @ y112.7
    "gender":           (405, 113, 557, 123, "rtl"),    # label النوع: ink 560-577
    "issue_date":       (205, 113, 352, 123, "rtl"),    # label تاريخ الإصدار: ink 355-399
    "expiry_date":      (20, 113, 130, 123, "rtl"),     # label تاريخ انتهاء الصلاحية: ink 133-199
    "dob":              (405, 124, 535, 134, "rtl"),    # label تاريخ الميلاد: ink 538-577
    "place_of_birth":   (205, 124, 360, 134, "rtl"),    # label محل الميلاد: ink 363-399
    "country_of_birth": (20, 124, 166, 134, "rtl"),     # label بلد الميلاد: ink 169-199
    "nationality":      (405, 134, 528, 144, "rtl"),    # label الجنسية: ink 531-577
    "other_nationality": (205, 134, 326, 144, "rtl"),   # label هل لديك جنسيات اخرى: ink 329-399
    "customer_type":    (405, 145, 535, 155, "rtl"),    # label نوعية العميل: ink 538-577
    "disability":       (205, 145, 322, 155, "rtl"),    # label هل العميل من ذوى الهمم؟ ink 325-399
    "address":          (100, 183, 549, 193, "rtl"),    # label العنوان: ink 552-574
    "country":          (405, 193, 558, 203, "rtl"),    # label البلد: ink 561-574
    # section 2 - correspondence
    "mail_address":     (100, 231, 549, 241, "rtl"),
    "mail_country":     (405, 242, 558, 252, "rtl"),
    "statement_freq":   (360, 252, 507, 262, "rtl"),    # label دورية كشف الحساب: ink 510-574
    "statement_lang":   (40, 252, 145, 262, "rtl"),     # label لغة المراسلات: ink 148-192
    "home_phone":       (280, 267, 532, 277, "rtl"),    # label هاتف المنزل: ink 535-574
    "home_cc":          (200, 267, 246, 277, "rtl"),    # label كود البلد: ink 249-273
    "mobile":           (410, 277, 527, 287, "rtl"),    # label هاتف المحمول: ink 530-574
    "mobile_cc":        (330, 277, 379, 287, "rtl"),    # label كود البلد: ink 382-406
    "mobile2":          (125, 277, 266, 287, "rtl"),    # label هاتف المحمول 2: ink 269-324
    "mobile2_cc":       (30, 277, 91, 287, "rtl"),      # label كود البلد: ink 94-118
    "email":            (250, 292, 520, 302, "ltr-right"),  # label البريد الإلكتروني: ink 523-574
    # section 3 - employment
    "profession":       (395, 343, 552, 353, "rtl"),    # label المهنة: ink 555-574
    "employer":         (253, 376, 489, 385.5, "rtl"),  # on underline 252.1-489.3 @ y385.8
    "employment_start": (35, 376, 180, 385.5, "rtl"),   # on underline 34.0-180.5 @ y385.8
    "employer_address": (31, 392, 495, 402, "rtl"),     # on underline 30.5-495.3 @ y402.4
    "employer_country": (361, 403, 511, 413, "rtl"),    # on underline 360.9-511.8 @ y413.2
    "employer_phone":   (30, 403, 131, 413, "rtl"),     # on underline 29.8-131.3 @ y413.2
    # section 5 - social status
    "marital_status":   (392, 598, 517, 608, "rtl"),    # label الحالة الاجتماعية: ink 520-574
    "residence_country": (250, 598, 356, 608, "rtl"),   # label بلد الإقامة: ink 359-387
}

# field -> {option value: checkbox cell (x0, y0, x1, y1)}
CHECKBOXES = {
    "housing": {
        "إيجار": (502.8, 171.6, 520.3, 182.1),
        "تمليك": (413.0, 171.6, 432.6, 182.1),
    },
    "work_sector": {
        "قطاع عام": (497.6, 326.3, 512.5, 336.6),
        "قطاع خاص": (435.7, 326.3, 451.2, 336.6),
        "شرطة": (368.6, 326.3, 383.6, 336.6),
        "قوات مسلحة": (313.3, 326.3, 329.9, 336.6),
        "اعمال حره": (239.6, 326.3, 254.6, 336.6),
        "طالب": (176.4, 326.3, 193.2, 336.6),
        "لا يعمل": (116.5, 326.3, 131.5, 336.6),
        "بالمعاش": (57.0, 326.3, 70.6, 336.6),
    },
    "job_level": {
        "إدارة عليا": (468.0, 360.0, 483.0, 370.4),
        "إدارة وسطى": (389.1, 360.0, 406.5, 370.4),
        "وظائف نمطية وتنفيذية": (301.5, 360.0, 315.7, 370.4),
    },
    "income_source": {
        "ميراث": (474.2, 420.0, 489.8, 430.4),
        "اعمال حره": (396.4, 420.0, 412.2, 430.4),
        "أراضي": (317.4, 420.0, 332.9, 430.4),
        "راتب شهري": (244.7, 420.0, 260.6, 430.4),
        "أخرى": (165.5, 420.0, 181.1, 430.4),
    },
    "income_band": {  # 11 options in a 4-column grid
        "أقل من 5 الف جم": (551.7, 441.6, 566.0, 452.1),
        "5 الف جم وأقل من 10 الف جم": (551.7, 452.6, 566.0, 462.9),
        "10 الف جم وأقل من 20 الف جم": (551.7, 463.4, 566.0, 473.8),
        "20 الف جم وأقل من 30 الف جم": (416.1, 441.6, 430.6, 452.1),
        "30 الف جم وأقل من 70 الف جم": (416.1, 452.6, 430.6, 462.9),
        "70 الف جم وأقل من 100 الف جم": (416.1, 463.4, 430.6, 473.8),
        "100 الف جم وأقل من 200 الف جم": (278.1, 441.6, 292.6, 452.1),
        "200 الف جم وأقل من 300 الف جم": (278.1, 452.6, 292.6, 462.9),
        "300 الف جم وأقل من 400 الف جم": (278.1, 463.4, 292.6, 473.8),
        "400 الف جم وأقل من مليون جم": (132.5, 441.6, 147.1, 452.1),
        "أكثر من مليون جم": (132.5, 452.6, 147.1, 462.9),
    },
    "other_banks": {
        "لا": (375.4, 523.4, 387.7, 534.9),
        "نعم": (280.6, 523.4, 294.1, 534.9),
    },
    "residency": {
        "مواطن مقيم": (485.7, 608.2, 502.4, 618.7),
        "مواطن غير مقيم": (369.7, 608.2, 386.2, 618.7),
        "أجنبي مقيم": (252.6, 608.2, 269.3, 618.7),
        "أجنبي غير مقيم": (134.1, 608.2, 149.9, 618.7),
    },
    "education": {
        "أمي": (542.5, 629.9, 561.5, 640.3),
        "تعليم أساسي": (425.7, 629.9, 444.9, 640.3),
        "مؤهل متوسط": (309.0, 629.9, 328.3, 640.3),
        "مؤهل فوق المتوسط": (192.1, 629.9, 209.2, 640.3),
        "مؤهل عالي": (542.5, 640.8, 561.5, 651.2),
        "دراسات عليا": (425.7, 640.8, 444.9, 651.2),
        "دكتوراه": (309.0, 640.8, 328.3, 651.2),
    },
}
