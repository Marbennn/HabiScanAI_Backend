"""
URL configuration for habiscan_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from .views import home, public_images
from rest_framework_simplejwt.views import TokenRefreshView
from authBE.mysite.views import (
    RegisterView, ActivateView, CustomTokenObtainPairView,
    HelloProtectedView, PasswordResetRequestView,
    PasswordResetConfirmView, SignOutView,
    GoogleLoginView, GoogleSignupView
)

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/images/public/', public_images, name='public_images'),
    path('api/history/', include('imagehistory.urls')),
    # Auth endpoints from authBE/mysite
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/protected/', HelloProtectedView.as_view(), name='protected'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('auth/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('auth/signout/', SignOutView.as_view(), name='signout'),
    path('auth/api/auth/social/login/', GoogleLoginView.as_view(), name='google_login'),
    path('auth/api/auth/social/signup/', GoogleSignupView.as_view(), name='google_signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)