from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import SignUpView
from . import views

urlpatterns = [
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('password_reset/sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    url(r'^profile/', views.user_profile, name='user_profile'),
    # url(r'^order/(?P<order_id>[-\w]+)/$', views.user_order_detail, name='user_order_detail'),
]
