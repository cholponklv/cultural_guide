from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user import views
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('signup/', views.UserRegistrationView.as_view(),name ='signup'),
    path('profile/',views.UserProfileView.as_view(),name = 'profile')
]