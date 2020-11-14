from django.urls import path
from .views import RegistrationView, LoginView, ActivateAccountView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="accounts-register"),
    path('login/', LoginView.as_view(), name="accounts-login"),
    path('activate/<uidb64>/<token>',
         ActivateAccountView.as_view(), name="accounts-activate")

]
