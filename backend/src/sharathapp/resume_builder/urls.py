from django.conf.urls import *
from rest_framework.routers import *

from .views import *

router = DefaultRouter()

router.register('resume', ResumeViewSet, base_name="resume")

urlpatterns = [
    url(r'^', include(router.urls)),
]
