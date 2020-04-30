from  django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import Home, SinPrivilegios
urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('login/',auth_views.LoginView.as_view(template_name='bases/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('sinprivilegios/', SinPrivilegios.as_view(), name='sinprivilegios')
]