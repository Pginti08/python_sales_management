from rest_framework.routers import DefaultRouter
from . import views  # import your views file

router = DefaultRouter()
router.register(r'admin/bankdetails', views.AdminBankDetailViewSet, basename='admin-bankdetails')
router.register(r'admin/businessdetails', views.AdminBusinessDetailViewSet, basename='admin-businessdetails')
router.register(r'admin/invoices', views.AdminInvoiceViewSet, basename='admin-invoices')
router.register(r'admin/clients', views.AdminClientViewSet, basename='admin-clients')
router.register(r'admin/projects', views.AdminProjectViewSet, basename='admin-projects')
router.register(r'admin/users', views.AdminUserProfileViewSet, basename='admin-users')

urlpatterns = router.urls
