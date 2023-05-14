from .views import RegistrationView, UsernameRegistrationView, EmailRegistrationView, VerificationView, LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from django.urls import path

urlpatterns=[
    path('register',RegistrationView.as_view(),name='register'),
    path('validate-username',csrf_exempt(UsernameRegistrationView.as_view()),name='validate-username'),
    path('validate-email',csrf_exempt(EmailRegistrationView.as_view()),name='validate-email'),
    path('activate/<uidb64>/<token>',(VerificationView.as_view()),name='activate'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
]