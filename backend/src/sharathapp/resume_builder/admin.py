from django.contrib import admin
from .models import *
from .forms import ResumeForm


class EducationInline(admin.TabularInline):
    model = Education
    fields = ['resume', 'institution', 'degree', 'start', 'graduation', 'text']
    extra =1

class SkillInline(admin.TabularInline):
    model = Skill
    fields = ['resume', 'name', 'level', 'text']
    extra =1

class ExperienceInline(admin.TabularInline):
    model = Experience
    fields = ['resume', 'institution', 'title', 'start_date', 'end_date', 'still_working', 'text']
    extra =1

class ProjectsInline(admin.TabularInline):
    model = Projects
    fields = ['resume', 'title', 'text']
    extra =1

class ResumeAdmin(admin.ModelAdmin):
    form = ResumeForm
    inlines = [EducationInline, SkillInline, ExperienceInline, ProjectsInline]
    
    list_display = ('id', 'user',)



# Register your models here.
admin.site.register(Resume, ResumeAdmin)
