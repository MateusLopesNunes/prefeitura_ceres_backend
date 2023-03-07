from django.urls import path
from . import views

urlpatterns = [
  path('', views.getRoutes),
  path('reqs/', views.GetRequests.as_view()),
  path('create/', views.CreateReq.as_view()),
  path('types/', views.GetRequestsType.as_view()),
  path('create/type/', views.createRequestType.as_view()),
  path('<str:pk>/delete/type/', views.deleteRequestType.as_view()),
  path('status/', views.GetStatus.as_view()),
  path('status/user/<str:pk>', views.GetUserRequestStatus.as_view()),
  path('status/code', views.GetStatusList.as_view()),
  path('create/status/', views.CreateStatus.as_view()),
  path('<str:pk>/update/', views.UpdateReq.as_view()),
  path('<str:pk>/cancel/', views.cancel_req),
  path('<str:pk>/delete/', views.DeleteReq.as_view()),
  path('<str:pk>/', views.GetRequest.as_view()),
  path('<str:pk>/status/', views.GetRequestStatus.as_view()),
  path('<str:pk>/user/', views.GetUserRequests.as_view()),
] 