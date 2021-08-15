from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db import transaction

from .forms import UserForm, ProfileForm, SignUpForm


# from orders.models import Order
# from shop.views import Category


# @login_required
# def user_order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     categories = Category.objects.all()
#     category_set = []
#     for category in categories:
#         for item in order.items.all():
#             if item.product.category == category and category not in category_set:
#                 category_set.append(category)
#
#     return render(request,
#                   'order/user_order_detail.html',
#                   {'order': order, 'category_set': category_set})
#

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/registration/signup.html'


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as  {username}.")
                return redirect("homepage")
            else:
                messages.error(request, "You have entered incorrect username or password.")
        else:
            messages.error(request, "You have entered incorrect username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="accounts/registration/login.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You are logged out.")
    return redirect("homepage")


@login_required
def user_profile(request):
    return render(request, 'accounts/profile.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password reset request"
                    email_template_name = "accounts/registration/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'ilvits.com',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@ilvits.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/registration/password_reset_form.html",
                  context={"password_reset_form": password_reset_form})


@login_required
@transaction.atomic
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES or None, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Updated!')
            return redirect('accounts:user_profile')
        else:
            messages.error(request, 'Please correct errors.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
