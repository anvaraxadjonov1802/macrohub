from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Mavzular, Modullar, AmaliyMavzu, AmaliyModul, TestSavol, TestModul, TestNatija, Topshiriq, YuborilganTopshiriq, TopshiriqModul
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from django.http import HttpResponse
from django.contrib import messages


def nazariy(request):
    modullar = Modullar.objects.prefetch_related('mavzular_set').all()
    return render(request, 'macros/nazariy.html', {'modullar': modullar})


def mavzu_detail(request, pk):
    mavzu = get_object_or_404(Mavzular, pk=pk)
    return render(request, 'macros/mavzu_detail.html', {'mavzu': mavzu})


def amaliy(request):
    mavzular = AmaliyMavzu.objects.all()
    modullar = AmaliyModul.objects.all()
    context = {
        'mavzular': mavzular,
        'modullar': modullar,
    }
    return render(request, 'macros/amaliy.html', context)


def amaliy_mavzu_detail(request, pk):
    mavzu = get_object_or_404(AmaliyMavzu, pk=pk)
    return render(request, 'macros/amaliy_detail.html', {'mavzu': mavzu})


def video_qism(request):
    # Barcha modullar va ularning videolari
    mavzular = AmaliyMavzu.objects.all()
    modullar = AmaliyModul.objects.all()
    context = {
        'mavzular': mavzular,
        'modullar': modullar,
    }
    return render(request, 'macros/video.html', context)


def video_detail(request, pk):
    video = get_object_or_404(AmaliyMavzu, pk=pk)
    return render(request, 'macros/video_detail.html', {'video': video})


def dashboard(request):
    mavzular = AmaliyMavzu.objects.all()
    modullar = AmaliyModul.objects.all()
    context = {
        'mavzular': mavzular,
        'modullar': modullar,
    }
    return render(request, 'macros/index.html', context)


def amaliy_mavzu_pdf(request, pk):
    mavzu = AmaliyMavzu.objects.get(pk=pk)
    template = get_template('macros/amaliy_pdf.html')
    html = template.render({'mavzu': mavzu})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{mavzu.title}.pdf"'

    pisa_status = pisa.CreatePDF(io.StringIO(html), dest=response)
    if pisa_status.err:
        return HttpResponse('PDF yaratishda xatolik yuz berdi')
    return response


# def test_finish_view(request, modul_id):
#     modul = TestModul.objects.get(id=modul_id)
#     savollar = modul.savollar.all()
#     foydalanuvchi_javoblari = request.POST  # Assume submitted answers
#
#     togrilar_soni = 0
#     for savol in savollar:
#         user_answer = foydalanuvchi_javoblari.get(str(savol.id))
#         if user_answer and user_answer == savol.correct_answer:
#             togrilar_soni += 1
#
#     return render(request, 'test/natija.html', {
#         'score': togrilar_soni,
#         'total': savollar.count(),
#     })


def test_list(request):
    testlar = TestModul.objects.all()
    return render(request, 'macros/test.html', {'testlar': testlar})


@login_required
def test_detail(request, test_id):
    modul = get_object_or_404(TestModul, id=test_id)
    savollar = modul.savollar.all()

    if request.method == 'POST':
        correct_answers = 0
        total_questions = savollar.count()

        for savol in savollar:
            user_answer = request.POST.get(f"savol_{savol.id}")
            if user_answer and user_answer.strip().lower() == savol.correct_answer.strip().lower():
                correct_answers += 1

        wrong_answers = total_questions - correct_answers
        score_percent = round((correct_answers / total_questions) * 100)

        # Baholash
        if score_percent >= 90:
            grade = "A'lo"
        elif score_percent >= 75:
            grade = "Yaxshi"
        elif score_percent >= 60:
            grade = "Qoniqarli"
        else:
            grade = "Qoniqarsiz"

        TestNatija.objects.create(
            user=request.user,
            modul=modul,
            correct_answers=correct_answers,
            wrong_answers=wrong_answers,
            score_percent=score_percent,
            grade=grade
        )
        # Natijani sahifaga yuborish
        return render(request, 'macros/test_result.html', {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'wrong_answers': wrong_answers,
            'score_percent': score_percent,
            'grade': grade,
            'modul': modul
        })

    return render(request, 'macros/test_detail.html', {
        'modul': modul,
        'savollar': savollar
    })


# Barcha topshiriqlar ro‘yxati
@login_required
def topshiriq_list(request):
    topshiriqlar = Topshiriq.objects.all().order_by('-created_at')
    return render(request, 'macros/topshiriqlar.html', {
        'topshiriqlar': topshiriqlar
    })


# Bitta topshiriq sahifasi (detal + yuborish formasi)
@login_required
def topshiriq_detail(request, topshiriq_id):
    topshiriq = get_object_or_404(Topshiriq, id=topshiriq_id)

    # Foydalanuvchining mavjud topshirgan javobi (agar bo‘lsa)
    existing_submission = YuborilganTopshiriq.objects.filter(
        user=request.user,
        topshiriq=topshiriq
    ).first()

    # Faqat "rejected" bo‘lsa qayta topshirish mumkin
    can_submit = not existing_submission or existing_submission.status == 'rejected'

    if request.method == 'POST' and can_submit:
        solution_file = request.FILES.get('solution_file')
        comment = request.POST.get('comment')

        # Agar oldingi rejected bo‘lsa, yangisini yaratmasdan yangilaymiz
        if existing_submission and existing_submission.status == 'rejected':
            existing_submission.solution_file = solution_file
            existing_submission.comment = comment
            existing_submission.status = 'pending'  # yana ko‘rib chiqish uchun
            existing_submission.save()
        else:
            YuborilganTopshiriq.objects.create(
                user=request.user,
                topshiriq=topshiriq,
                solution_file=solution_file,
                comment=comment
            )

        messages.success(request, "Topshiriq muvaffaqiyatli yuborildi!")
        return redirect('topshiriq_detail', topshiriq_id=topshiriq.id)

    return render(request, 'macros/topshiriq_detail.html', {
        'topshiriq': topshiriq,
        'submission': existing_submission,
        'can_submit': can_submit,
    })