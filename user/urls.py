from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from user import views

router = DefaultRouter()
router.register('users', viewset=views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('signup/', views.UserRegistrationView.as_view(),name ='signup'),
    path('signup/company/', views.CompanyRegistrationView.as_view(),name ='signup_company'),
    path('profile/',views.UserProfileView.as_view(),name = 'profile'),
    path('add_to_favourites/', views.FavouritesCreateView.as_view(), name='add_to_favourites'),
    path('favourites/', views.FavouritesListAPIView.as_view(), name='favourites-list'),
]