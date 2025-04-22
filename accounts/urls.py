from django.urls import path
from .views import (
    SignupView,
    LoginView,
    LogoutAPIView,
    CategoryListCreateView,
    SendResetEmailView,
    ResetPasswordByEmailView,
    ResetPasswordView,
    SalesUserProfileRetrieveUpdateDestroyView
)

urlpatterns = [
    path('auth-signup/', SignupView.as_view(), name='signup'),
    path('auth-login/', LoginView.as_view(), name='login'),
    path('auth-logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth-category/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('auth-send-reset-email/', SendResetEmailView.as_view(), name='send-reset-email'),
    path('reset-password-by-email/', ResetPasswordByEmailView.as_view(), name='reset-password-by-email'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/', SalesUserProfileRetrieveUpdateDestroyView.as_view(), name='business-detail'),
]
