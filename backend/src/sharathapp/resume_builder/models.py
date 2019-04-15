from django.db import models
from month.models import MonthField

from .fields import MinMaxRangeField
from accounts.models import User

# Create your models here.

class Resume(models.Model):
    """
    Create a custom user using django base user model.
    """
    user = models.ForeignKey(User)
    bio = models.TextField(help_text="Please enter few words which would best describe you.")

    def __str__(self):
        return self.user.first_name

class Education(models.Model):

    resume = models.ForeignKey(Resume)
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    graduation = MonthField("Month Value", help_text="Year-month of graduation") 
    start = MonthField("Month Value", help_text="Year-month of start") 
    text = models.TextField(help_text="Please enter few words regarding the education in the institute.")

class Skill(models.Model):

    resume = models.ForeignKey(Resume)
    name = models.CharField(max_length=100)
    # level = models.IntegerField(default=3, validators=[MinValueValidator(0),MaxValueValidator(850)])
    level = MinMaxRangeField(default=3, min_value=1, max_value=5)
    text = models.TextField(help_text="Please enter few words regarding the skill.",
            blank=True, null=True)


class Experience(models.Model):

    resume = models.ForeignKey(Resume)
    institution = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    start_date = MonthField("Month Value", help_text="Year-month of start") 
    end_date = MonthField("Month Value", help_text="Year-month of end", null=True, blank=True)
    still_working = models.BooleanField(default=False)
    text = models.TextField(help_text="Please enter few words regarding the work in the institute.")

class Projects(models.Model):

    resume = models.ForeignKey(Resume)
    title = models.CharField(max_length=100)
    text = models.TextField(help_text="Please enter few words regarding the project.")
