from django.urls import path
from . import views
urlpatterns = [
     path('registration/', views.user_register_api_view),
    path('confirm/', views.confirm_user_api_view), 


]