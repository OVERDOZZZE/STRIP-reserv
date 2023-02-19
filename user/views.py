from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView
from rest_framework import status, authentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import RegisterUserForm
from .models import *
from django.contrib.auth import logout, login, get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .utils import DataMixin


from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

from .serializers import UserValidateSerializer, UserCreateSerializer, User


def user_profile(request):
    error = 'No user'
    if request.user:
        user = get_object_or_404(CustomUser, id=request.user.id)
        if request.user.avatar:
            avatar = get_object_or_404(Avatar, id=request.user.avatar.id)
            context = {
                'user': user,
                'avatar': avatar
            }
        else:
            context = {
                'user': user
            }
    else:
        context = {
            'user': error
        }
    return render(request, 'user/user_profile.html', context=context)


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="NameSite")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


# class RegisterUser(DataMixin, CreateView):
#     form_class = RegisterUserForm
#     template_name = 'user/register.html'
#     success_url = reverse_lazy('user_profile')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="NameSite")
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('user_profile')

def activate(request, uid64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalidd')

    return redirect('user_profile')


def activateEmail(request, user, to_email):
    main_subject = 'Activate your user account'
    message = render_to_string('user/activate_account.html',
        {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }
    )
    email = EmailMessage(main_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            if user.is_active:
                return redirect('home')
            else:
                confirmation = 'Please check your email to confirm signing up'
                if user.is_active:
                    return redirect('login')
                else:
                    return render(request, 'user/login.html', {'confirmation': confirmation})

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = RegisterUserForm()

    return render(
        request=request,
        template_name="user/register.html",
        context={"form": form}
        )


def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')


@api_view(['POST'])
def register(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    CustomUser.objects.create_user(**serializer.validated_data)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def authorization(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_403_FORBIDDEN)