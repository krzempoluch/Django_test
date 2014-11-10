from django.db import models
from rest_framework import routers, serializers, viewsets

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
    
    def addMwd(self, mwd):
        mwdToAdd = MWD.objects.filter(name=mwd['name'])
        self.MWDs.add(mwdToAdd[0])
    
class MWDSerializer(serializers.ModelSerializer):
    class Meta:
        model = MWD
        fields = ('id', 'name', 'issue_date')
                
class ProjektSerializer(serializers.ModelSerializer):
    MWDs = MWDSerializer(many=True)
    class Meta:
        model = Projekt
        fields = ('id', 'name', 'jira_URL', 'start_date', 'MWDs')   
        
class MWDViewSet(viewsets.ModelViewSet):
    queryset = MWD.objects.all()
    serializer_class = MWDSerializer
  
class ProjektViewSet(viewsets.ModelViewSet):
    queryset = Projekt.objects.all()
    serializer_class = ProjektSerializer  