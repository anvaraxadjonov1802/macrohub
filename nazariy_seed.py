import os
import django
import sys

# sys.path'ga root loyihani qo‘shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# DJANGO_SETTINGS_MODULE ni to‘g‘ri nom bilan belgilang
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macrohub.settings")

# Django'ni ishga tushiramiz
django.setup()


from macros.models import Modullar, Mavzular

# Ma'lumotlarni tozalash (ixtiyoriy)
Modullar.objects.all().delete()
Mavzular.objects.all().delete()

modullar = {
    "Excel asoslari": [
        {
            "title": "1. Kirish va interfeys bilan tanishuv",
            "content": "Excel dasturining asosiy interfeysi, menyulari va asosiy qismlar bilan tanishish.",
            "code_example": "",
            "explanation": "Excel oynasi, formula paneli, qatordan iborat struktura.",
        },
        {
            "title": "2. Hujayra va ustunlar bilan ishlash",
            "content": "Hujayralarni tanlash, ko‘chirish, formatlash.",
            "code_example": "",
            "explanation": "Ctrl + C / Ctrl + V kabi tezkor tugmalarni o‘rganing.",
        },
        {
            "title": "3. Formulalar bilan ishlash",
            "content": "Excel’da oddiy matematik amallar: qo‘shish, ayirish, ko‘paytirish.",
            "code_example": "=A1+B1",
            "explanation": "Formulalar = belgisidan boshlanadi.",
        },
        {
            "title": "4. Avtomatik to‘ldirish (AutoFill)",
            "content": "Raqamlar yoki matnlar ketma-ketligini avtomatik to‘ldirish.",
            "code_example": "",
            "explanation": "Pastki o‘ng burchakdagi kvadratni torting.",
        },
        {
            "title": "5. Nisbiy va absolyut havolalar",
            "content": "Formuladagi A1 va $A$1 farqlari.",
            "code_example": "=A1*$B$1",
            "explanation": "$ belgisidan foydalanilsa, absolyut bo‘ladi.",
        },
    ],
    "Ma'lumotlarni formatlash": [
        {
            "title": "6. Hujayralarni ranglash",
            "content": "Hujayralarga fon rangi, shrift rangi berish.",
            "code_example": "",
            "explanation": "Home > Fill Color orqali bajariladi.",
        },
        {
            "title": "7. Chegaralar va shriftlar bilan ishlash",
            "content": "Hujayra chegaralari, shrift o‘lchami va stili.",
            "code_example": "",
            "explanation": "Home > Font paneli orqali sozlash mumkin.",
        },
        {
            "title": "8. Shartli formatlash",
            "content": "Qiymatga qarab avtomatik ranglash.",
            "code_example": "",
            "explanation": "Home > Conditional Formatting menyusi.",
        },
        {
            "title": "9. Jadval dizayni va uslublar",
            "content": "Jadvalni professional ko‘rinishga keltirish.",
            "code_example": "",
            "explanation": "Insert > Table funksiyasi.",
        },
        {
            "title": "10. Format Painter vositasi",
            "content": "Bir hujayraning formatini boshqasiga nusxalash.",
            "code_example": "",
            "explanation": "Home > Format Painter orqali ishlaydi.",
        },
    ],
}

for modul_nomi, mavzular in modullar.items():
    modul = Modullar.objects.create(title=modul_nomi)
    for index, mavzu in enumerate(mavzular, start=1):
        Mavzular.objects.create(
            modul=modul,
            title=mavzu["title"],
            content=mavzu["content"],
            code_example=mavzu["code_example"],
            explanation=mavzu["explanation"],
            order=index
        )

print("✅ 10 ta nazariy mavzu bazaga muvaffaqiyatli qo‘shildi.")
