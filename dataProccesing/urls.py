from rest_framework.routers import DefaultRouter
from dataProccesing.views import DataView

router = DefaultRouter()
router.register(r'data', DataView.as_view())

urlpatterns = router.urls
