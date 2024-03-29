"""charity_donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from charity_app.views import (
    LandingPageView,
    LoginView,
    LogoutView,
    RegisterView,
    AddDonationView,
    ConfirmationView,
    UserProfileView,
    SettingsView,
    ChangePasswordView,
    UpdateUserProfileView,
    ConfirmPasswordView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('add_donation/', AddDonationView.as_view(), name='add-donation'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),
    path('user_profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('update_profile/<int:user_id>/', UpdateUserProfileView.as_view(), name='update-profile'),
    path('confirm_password/<int:user_id>/', ConfirmPasswordView.as_view(), name='confirm-password'),
]
