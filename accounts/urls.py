from django.urls import path
from .views import (
    SignupView,
    login_view,
    LogoutView,
    CategoryListCreateView,
    SendResetEmailView,
    ResetPasswordByEmailView,
    ResetPasswordView,
    SalesUserProfileRetrieveUpdateDestroyView, AdminUserListView, AdminUserProfileView, SelfUserProfileView
)

urlpatterns = [
    path('auth-signup/', SignupView.as_view(), name='signup'),
    path('auth-login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth-category/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('auth-send-reset-email/', SendResetEmailView.as_view(), name='send-reset-email'),
    path('reset-password-by-email/', ResetPasswordByEmailView.as_view(), name='reset-password-email'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset-password'),
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/user/<int:pk>/', AdminUserProfileView.as_view(), name='admin-user-detail'),
    path('user/', SelfUserProfileView.as_view(), name='self-user-profile'),

]
