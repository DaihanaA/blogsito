from django.urls import path
from . import views  # Importa las vistas correspondientes para las autenticaciones

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    
]