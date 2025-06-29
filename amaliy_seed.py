import os
import sys
import django

# Loyihaning root katalogini sys.path ga qo‘shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django sozlamalarini yuklaymiz
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macrohub.settings")
django.setup()

from macros.models import AmaliyModul, AmaliyMavzu

# Avvalgi ma'lumotlarni tozalash (ixtiyoriy)
AmaliyModul.objects.all().delete()
AmaliyMavzu.objects.all().delete()

modullar = {
    "Excel amaliy mashg‘ulotlari": [
        {
            "title": "1. Oddiy hisob-kitob jadvalini yaratish",
            "task_description": "Excelda oylik ish haqini hisoblash jadvalini tuzish.",
            "step_by_step_guide": "Yangi fayl oching. Ishchi varaqqa ustunlar kiriting: Ism, Lavozim, Ish haqi, Bonus. Har bir xodim uchun qiymat kiriting. Umumiy ish haqini hisoblash uchun formuladan foydalaning: Ish haqi + Bonus.",
            "code_example": "=B2+C2",
            "explanation": "Formulalar orqali ustunlarni avtomatik hisoblash oson va tez.",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        {
            "title": "2. Shartli formatlash bilan ish haqi ajratish",
            "task_description": "Ish haqi 5 milliondan yuqori bo‘lgan xodimlarni qizil bilan belgilash.",
            "step_by_step_guide": "Ish haqi ustunini belgilang. Conditional Formatting menyusiga kiring. Yangi qoidani tanlang. Formula kiriting: =B2>5000000. Formatda qizil rangni tanlang.",
            "code_example": "",
            "explanation": "Shartli formatlash yordamida muhim ma'lumotlarni ajratish mumkin.",
            "video_url": "https://www.youtube.com/watch?v=V-_O7nl0Ii0",
        },
    ],
    "VBA bilan amaliyot": [
        {
            "title": "3. Oddiy VBA makros yozish",
            "task_description": "Tugma bosilganda 'Salom dunyo!' xabari chiqadigan VBA makros yozish.",
            "step_by_step_guide": "Alt + F11 tugmasini bosing. Yangi modul oching. Quyidagi kodni kiriting. Excel fayliga tugma joylashtiring. Tugmaga yozilgan kodni bog‘lang.",
            "code_example": 'Sub HelloWorld()\n    MsgBox "Salom dunyo!"\nEnd Sub',
            "explanation": "VBA yordamida oddiy avtomatlashtirish ishlarini bajarish mumkin.",
            "video_url": "https://www.youtube.com/watch?v=MtN1YnoL46Q",
        },
    ]
}

# Ma'lumotlarni saqlash
for modul_nomi, mavzular in modullar.items():
    modul = AmaliyModul.objects.create(name=modul_nomi)
    for index, mavzu in enumerate(mavzular, start=1):
        AmaliyMavzu.objects.create(
            modul=modul,
            title=mavzu["title"],
            task_description=mavzu["task_description"],
            step_by_step_guide=mavzu["step_by_step_guide"],
            code_example=mavzu.get("code_example", ""),
            explanation=mavzu.get("explanation", ""),
            video_url=mavzu.get("video_url", ""),
            order=index,
        )

print("✅ Amaliy mavzular bazaga muvaffaqiyatli qo‘shildi.")
