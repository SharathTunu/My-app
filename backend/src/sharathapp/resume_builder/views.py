from rest_framework.viewsets import ModelViewSet
from django.utils import timezone
from .models import *
from .render import Render
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class ResumeViewSet(ModelViewSet):
    permission_classes=()
    queryset = Resume.objects.all()
    def list(self, request, *args, **kwargs):
        resume = self.queryset.filter(id=1)#self.queryset.filter(user=self.request.user)
        if resume:
            params = {'resume':resume}
            return Render.render('templates/resume_builder/template1.html', params)
        else:
            return Response({'error':'There are no resumes'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)