import os
import sys
import django

# Loyihaning root katalogini sys.path ga qo‘shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django sozlamalarini yuklaymiz
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macrohub.settings")
django.setup()

from macros.models import TestModul, TestSavol

# Avvalgi ma'lumotlarni tozalash (ixtiyoriy)
TestSavol.objects.all().delete()
TestModul.objects.all().delete()

test_data = {
    "Excel asoslari": [
        {
            "question": "Excel formulasining boshlanish belgisi nima?",
            "option_a": "+",
            "option_b": "=",
            "option_c": "*",
            "option_d": "#",
            "correct_answer": "B"
        },
        {
            "question": "A1 va $A$1 orasidagi farq nimada?",
            "option_a": "Ikkalasi ham bir xil",
            "option_b": "A1 nisbiy, $A$1 absolyut",
            "option_c": "$A$1 nisbiy, A1 absolyut",
            "option_d": "Farqi yo‘q",
            "correct_answer": "B"
        },
    ],
    "Formatlash": [
        {
            "question": "Conditional Formatting qaysi menyuda joylashgan?",
            "option_a": "Insert",
            "option_b": "Data",
            "option_c": "Home",
            "option_d": "View",
            "correct_answer": "C"
        },
        {
            "question": "Format Painter vazifasi nima?",
            "option_a": "Matnni o‘chirish",
            "option_b": "Formatni nusxalash",
            "option_c": "Grafik chizish",
            "option_d": "Hisoblash",
            "correct_answer": "B"
        }
    ]
}

# Ma'lumotlarni saqlash
for modul_nomi, savollar in test_data.items():
    modul = TestModul.objects.create(name=modul_nomi)
    for savol in savollar:
        TestSavol.objects.create(
            modul=modul,
            question=savol["question"],
            option_a=savol["option_a"],
            option_b=savol["option_b"],
            option_c=savol["option_c"],
            option_d=savol["option_d"],
            correct_answer=savol["correct_answer"]
        )

print("✅ Test savollari bazaga muvaffaqiyatli qo‘shildi.")
