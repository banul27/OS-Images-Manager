from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from images import views as image_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('users/', include('users.urls')),
    path('images/', include('images.urls')),
    path('deployments/', include('deployments.urls')),
    path('', image_views.home),
]
