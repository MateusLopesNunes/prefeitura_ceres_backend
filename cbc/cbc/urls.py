from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from user.views import UsuariosViewSet, createUser
from rest_framework import routers
from django.views.static import serve
from user import views
from django.conf import settings
from django.conf.urls.static import static

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLUTTER_WEB_APP = os.path.join(BASE_DIR, 'flutter_web_app')

def flutter_redirect(request, resource):
    return serve(request, resource, FLUTTER_WEB_APP)


#router = routers.DefaultRouter()
#router.register('cadastrar', UsuariosViewSet, basename='Cadastrar Usuário')

urlpatterns = [
    path('flutter_web_app/', lambda r: flutter_redirect(r, 'index.html')),
    path('flutter_web_app/<path:resource>', flutter_redirect),
    path('admin/', admin.site.urls),
    path('token/', views.generate_jwt),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('request/', include('request.urls')),
    path('user/', include('user.urls')),
    #path('', include(router.urls)),
    path('cadastrar_usuario/', createUser),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)