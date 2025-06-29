from django.db import models
from .helpers.youtube import *
from django.conf import settings  # custom user modelga havola


class Modullar(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Mavzular(models.Model):
    modul = models.ForeignKey(Modullar, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    code_example = models.TextField(blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    file_attachment = models.FileField(upload_to='nazariy_qisim_fayllari/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AmaliyModul(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AmaliyMavzu(models.Model):
    modul = models.ForeignKey(AmaliyModul, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    task_description = models.TextField(help_text="Bu darsda nima o'rganiladi")
    step_by_step_guide = models.TextField(help_text="Bosqichma-bosqich qanday qilish")
    code_example = models.TextField(blank=True, null=True, help_text="Agar VBA kodi kerak bo‘lsa")
    explanation = models.TextField(blank=True, null=True, help_text="Qo‘shimcha tushuntirish yoki eslatma")
    file_attachment = models.FileField(upload_to='amaliy_fayllar/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_embed_url(self):
        if "shorts/" in self.video_url:
            return self.video_url.replace("shorts/", "embed/")
        elif "watch?v=" in self.video_url:
            return self.video_url.replace("watch?v=", "embed/")
        return self.video_url

    def get_video_id(self):
        match = re.search(r"(?:v=|\/shorts\/|\/embed\/)([a-zA-Z0-9_-]{11})", self.video_url)
        return match.group(1) if match else None

    def get_thumbnail_url(self):
        video_id = self.get_video_id()
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/0.jpg"
        return ""

    @property
    def step_guide_list(self):
        return [s.strip() for s in self.step_by_step_guide.split('.') if s.strip()]

    @property
    def video_duration(self):
        return get_video_duration(self.video_url, self.get_video_id())

    def __str__(self):
        return self.title


class TestModul(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TestSavol(models.Model):
    modul = models.ForeignKey(TestModul, on_delete=models.CASCADE, related_name='savollar')
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return self.question


class TestNatija(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modul = models.ForeignKey("TestModul", on_delete=models.CASCADE)
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    score_percent = models.IntegerField()
    grade = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.modul} - {self.score_percent}%"



class TopshiriqModul(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Topshiriq(models.Model):
    modul = models.ForeignKey(TopshiriqModul, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)
    example_file = models.FileField(upload_to='topshiriq_examples/', blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class YuborilganTopshiriq(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topshiriq = models.ForeignKey(Topshiriq, on_delete=models.CASCADE)
    solution_file = models.FileField(upload_to='yechimlar/')
    comment = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Yuborilgan'),
        ('reviewed', 'Tekshirilgan'),
        ('rejected', 'Qaytarilgan'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user} - {self.topshiriq.title}"

