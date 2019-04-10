from django.conf.urls import *
from rest_framework.routers import *

from .views import *

router = DefaultRouter()

router.register('user', UserViewSet, base_name="user")

urlpatterns = [
    url(r'^', include(router.urls)),
]
