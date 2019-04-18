from rest_framework.viewsets import ModelViewSet
from django.utils import timezone
from .models import *
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
# Create your views here.

class ResumeViewSet(ModelViewSet):
    permission_classes=()
    queryset = Resume.objects.all()
    def list(self, request, *args, **kwargs):
        resume = self.queryset.filter(id=1)[0]#self.queryset.filter(user=self.request.user)
        if resume:
            params = {'resume':resume,
            'skills': resume.skill_set.all(),
            'schools': resume.education_set.all(),
            'experience': resume.experience_set.all(),
            'projects': resume.projects_set.all()}
            html = render_to_string('resume_builder/template1.html', params)
            pdf = HTML(string=html).write_pdf()
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=certificate'+'.pdf'
            return response
        else:
            return Response({'error':'There are no resumes'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)