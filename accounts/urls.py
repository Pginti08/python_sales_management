from django.urls import path
from .views import send_reset_email, reset_password_by_email, signup_view, login_view, category_list_create, \
    ResetPasswordView, SalesUserProfileRetrieveUpdateDestroyView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('category/', category_list_create, name='category-list-create'),
    path('send-reset-email/', send_reset_email),
    path('reset-password-by-email/', reset_password_by_email),
    path('reset_password/', ResetPasswordView.as_view(), name='reset-password'),


    # This will handle GET by ID, PUT/PATCH (update), and DELETE
    path('profile/', SalesUserProfileRetrieveUpdateDestroyView.as_view(), name='business-detail')
]
