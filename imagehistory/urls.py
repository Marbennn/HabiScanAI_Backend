from rest_framework.routers import DefaultRouter
from .views import ImageHistoryViewSet

router = DefaultRouter()
router.register(r'images', ImageHistoryViewSet, basename='imagehistory')

urlpatterns = router.urls