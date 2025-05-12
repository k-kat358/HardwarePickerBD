from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('base', views.base, name='base'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/',views.register,name='register'),
    path('login/',views.LOGIN,name='login'),
    path('logout/', views.LOGOUT, name='logout'),
    path('builder/', views.builder, name='builder'),
    path('products/', include('products.urls')),

    path('buildhub/', include('buildhub.urls')),

   path('userprofile/', include('userprofile.urls')),
    path('guides/', include('guides.urls')),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)