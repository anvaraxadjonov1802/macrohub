import os
import sys
import django
from datetime import datetime, timedelta

# Django loyihasini ishga tushirish uchun sozlashlar
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macrohub.settings")
django.setup()

from macros.models import TopshiriqModul, Topshiriq

# Eski ma'lumotlarni tozalash (ixtiyoriy)
Topshiriq.objects.all().delete()
TopshiriqModul.objects.all().delete()

topshiriq_data = {
    "Excel amaliy topshiriqlari": [
        {
            "title": "1. Ish haqi jadvali tuzish",
            "description": "Xodimlar uchun ish haqi va bonuslarni hisoblovchi jadval yarating.",
            "requirements": "Formulalardan foydalanilsin. Jadval chiroyli formatlansin.",
            "deadline": datetime.now() + timedelta(days=7)
        },
        {
            "title": "2. Diagramma tuzish",
            "description": "Savdo natijalariga asoslangan diagramma yarating.",
            "requirements": "Bar chart yoki pie chart ishlatilsin.",
            "deadline": datetime.now() + timedelta(days=10)
        }
    ],
    "VBA topshiriqlari": [
        {
            "title": "3. VBA orqali 'Hello World' oynasi",
            "description": "Tugmani bosganda 'Hello World' oynasi chiqadigan VBA kod yozing.",
            "requirements": "Command Button yordamida ishlang.",
            "deadline": datetime.now() + timedelta(days=5)
        },
    ]
}

# Ma'lumotlarni bazaga yozish
for modul_nomi, topshiriqlar in topshiriq_data.items():
    modul = TopshiriqModul.objects.create(name=modul_nomi)
    for topshiriq in topshiriqlar:
        Topshiriq.objects.create(
            modul=modul,
            title=topshiriq["title"],
            description=topshiriq["description"],
            requirements=topshiriq.get("requirements", ""),
            deadline=topshiriq.get("deadline")
        )

print("✅ Topshiriqlar bazaga muvaffaqiyatli qo‘shildi.")
