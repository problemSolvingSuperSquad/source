from django.urls import path
from . import views
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView,)


urlpatterns = [
    path('routes/', views.getRoutes),
    path('images/', views.getImages),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register/', views.RegisterView.as_view(), name='auth_register'),
    path('imageSearch/', views.imageSearch),
    path('profile/', views.getProfile),
    path('locationSearch/', views.locationSearch),
    path('nameSearch/', views.nameSearch),
]