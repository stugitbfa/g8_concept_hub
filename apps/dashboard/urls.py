from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('email_verify/', views.email_verify, name='email_verify'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('index/',views.index, name='index' ),
    path('profile/',views.profile, name='profile' ),
] 