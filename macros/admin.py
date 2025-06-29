from django.contrib import admin
from .models import Modullar, Mavzular, AmaliyModul, AmaliyMavzu, TestModul, TestSavol, TestNatija, TopshiriqModul, Topshiriq, YuborilganTopshiriq

@admin.register(Modullar)
class ModullarAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

@admin.register(Mavzular)
class MavzularAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modul', 'order', 'created_at')
    list_filter = ('modul',)
    search_fields = ('title', 'content')
    ordering = ('modul', 'order')

@admin.register(AmaliyModul)
class AmaliyModulAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(AmaliyMavzu)
class AmaliyMavzuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modul', 'created_at', 'order')
    list_filter = ('modul', 'created_at')
    search_fields = ('title', 'task_description', 'step_by_step_guide', 'explanation', 'code_example')
    ordering = ('order',)
    readonly_fields = ('created_at',)


@admin.register(TestModul)
class TestModulAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(TestSavol)
class TestSavolAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'modul', 'correct_answer')
    search_fields = ('question',)
    list_filter = ('modul',)
    list_per_page = 20


@admin.register(TestNatija)
class TestNatijaAdmin(admin.ModelAdmin):
    list_display = ('user', 'modul', 'correct_answers', 'wrong_answers', 'score_percent', 'grade', 'created_at')
    list_filter = ('modul', 'grade', 'created_at')
    search_fields = ('user__username', 'modul__name')
    ordering = ('-created_at',)


@admin.register(TopshiriqModul)
class TopshiriqModulAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Topshiriq)
class TopshiriqAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modul', 'deadline', 'created_at')
    list_filter = ('modul',)
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

@admin.register(YuborilganTopshiriq)
class YuborilganTopshiriqAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'topshiriq', 'submitted_at', 'status')
    list_filter = ('status', 'submitted_at')
    search_fields = ('user__email', 'topshiriq__title')
    readonly_fields = ('submitted_at',)
