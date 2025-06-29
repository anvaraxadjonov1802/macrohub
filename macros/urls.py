# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('nazariy/', views.nazariy, name='nazariy_qisim'),
    path('amaliy/', views.amaliy, name='amaliy_qisim'),
    path('mavzu/<int:pk>/', views.mavzu_detail, name='mavzu_detail'),
    path('video/', views.video_qism, name='video_qism'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('amaliy/<int:pk>/', views.amaliy_mavzu_detail, name='amaliy_detail'),
    path('amaliy/<int:pk>/pdf/', views.amaliy_mavzu_pdf, name='amaliy_mavzu_pdf'),
    path('testlar/', views.test_list, name='test_list'),
    path('testlar/<int:test_id>/', views.test_detail, name='test_detail'),
    path('topshiriqlar/', views.topshiriq_list, name='topshiriq_list'),
    path('topshiriqlar/<int:topshiriq_id>/', views.topshiriq_detail, name='topshiriq_detail'),
]
