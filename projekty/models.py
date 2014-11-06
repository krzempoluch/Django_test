from django.db import models

# Create your models here.
class MWD(models.Model):
    name = models.CharField(max_length=200)
    issue_date = models.DateTimeField('data rozpoczecia dzialania MWD')
    def __str__(self):
        return "["+self.name+", "+str(self.issue_date)+"]"

class Projekt(models.Model):
    name = models.CharField(max_length=200)
    jira_URL = models.CharField(max_length=200)
    start_date = models.DateTimeField('data startu')
    MWDs = models.ManyToManyField(MWD)
    def __str__(self):
        return "["+self.name+", "+self.jira_URL+", "+str(self.start_date)+"]"
    