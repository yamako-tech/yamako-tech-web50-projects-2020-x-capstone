from django.urls import path
from . import views
from .admin import mypage_site



urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('mypage/', mypage_site.urls),
    path('mychart/', views.myChart, name='mychart'),
    path('myword/', views.mywordlist, name='myword'),
    path('save/', views.save_data, name='save'),
    path('delete/', views.delete_data, name='delete'),
    path('edit/', views.edit_data, name='edit'),
]
