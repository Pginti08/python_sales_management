from rest_framework.routers import DefaultRouter
from adminpanel.views import (
    AdminUserViewSet,
    AdminClientViewSet,
    AdminInvoiceViewSet,
    AdminProjectViewSet,
    AdminBusinessDetailViewSet,
    AdminBankDetailViewSet,
    AdminInvoiceItemViewSet,
    # AdminClientUserViewSet,       # ✅ new
    # AdminBusinessUserViewSet,     # ✅ new
)

router = DefaultRouter()

router.register(r'admin/users', AdminUserViewSet)
router.register(r'admin/clients', AdminClientViewSet)
router.register(r'admin/invoices', AdminInvoiceViewSet)
router.register(r'admin/projects', AdminProjectViewSet)
router.register(r'admin/businesses', AdminBusinessDetailViewSet)
router.register(r'admin/banks', AdminBankDetailViewSet)
router.register(r'admin/items', AdminInvoiceItemViewSet)

# ✅ new routes for user-based filtering
# router.register(r'admin/clients-by-user', AdminClientUserViewSet)
# router.register(r'admin/businesses-by-user', AdminBusinessUserViewSet)

urlpatterns = router.urls
