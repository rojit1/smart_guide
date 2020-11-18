from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import login, logout, authenticate

User = get_user_model()


class RegistrationView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')

        if len(password) < 8:
            messages.add_message(request, messages.ERROR,
                                 'password must be at least 8 chars')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'password doesnot match')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'provide a valid email')
            context['has_error'] = True

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Account with this email already exists')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Username with this email already exists')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'accounts/register.html', context)

        user = User.objects.create(
            username=username, email=email, first_name=firstname, last_name=lastname)
        user.set_password(password)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        email_subject = 'Activate your account'
        message = render_to_string('accounts/activate.html', {'user': user, 'domain': current_site.domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': generate_token.make_token(user)
                                                              })
        email_msg = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )
        email_msg.send()

        return render(request, 'accounts/verify.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            messages.add_message(request, messages.ERROR,
                                 'Both Username and password are required')
            context['has_error'] = True
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Invalid login')
            context['has_error'] = True
        if context['has_error']:
            return render(request, 'accounts/login.html', status=401, context=context)

        login(request, user)
        return redirect('dashboard:index')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None
        if user and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('accounts-login')

        return render(request, 'accounts/failed.html', status=401)


class logoutView(View):
    def post(self, request):
        logout(request)
        return redirect('accounts-login')
