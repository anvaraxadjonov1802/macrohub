from django.urls import path
from . import views

urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
    path('register/email/', views.register_email, name='register_email'),
    path('register/name/', views.register_name, name='register_name'),
    path('register/password/', views.register_password, name='register_password'),
    path('login/password/', views.login_password, name='login_password'),
    path('register/verify/', views.register_verify, name='register_verify'),
    path('register/complete/', views.register_complete, name='register_complete'),
]
