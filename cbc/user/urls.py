from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.getRoutes),
    path('create/', views.createUser),
    #path('signup/', views.ListaUsuarios.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('users/', views.GetUsers.as_view()),
    path('login/<str:cpf>', views.GetLogin.as_view()),
    path('<int:pk>/update', views.UpdateUser.as_view(), name="update_user"),
    path('<int:pk>/change_password', views.UpdatePass.as_view(), name="change_password"),
    path('<int:pk>/delete', views.DeleteUser.as_view()),
    path('<int:pk>/', views.GetUser.as_view()),
    path('reset_password/', views.resetPassword)
]