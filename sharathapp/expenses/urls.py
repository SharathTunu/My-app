from django.conf.urls import *
from rest_framework.routers import *

from .views import *

router = DefaultRouter()

router.register('transaction', TransactionViewSet, base_name="trnasaction")

urlpatterns = [
    url(r'^', include(router.urls)),
]
