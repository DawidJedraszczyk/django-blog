"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import SignupView, LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.utils.translation import gettext_lazy as _
from django.views.i18n import set_language
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('set_language/', set_language, name='set_language'),
    path('', include('apps.posts.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path(_('accounts/'), include('allauth.urls')),
    path(_('users/'), include('apps.users.urls')),
    path(_('accounts/signup/'), SignupView.as_view(), name='account_signup'),
    path(_('accounts/login/'), LoginView.as_view(), name='account_login'),
    path(_('accounts/logout/'), LogoutView.as_view(), name='account_logout'),
    path(_('accounts/password/change/'), PasswordChangeView.as_view(), name='account_change_password'),
    path(_('accounts/password/reset/'), PasswordResetView.as_view(), name='account_reset_password'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)