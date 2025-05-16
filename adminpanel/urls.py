from rest_framework.routers import DefaultRouter
from adminpanel.views import (
    AdminUserViewSet,
)

router = DefaultRouter()

router.register(r'admin/users', AdminUserViewSet)


urlpatterns = router.urls
