from django.conf.urls import patterns, url, include
from projekty.models import MWD, Projekt
from rest_framework import routers, serializers, viewsets

from projekty import views

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

router = routers.DefaultRouter()
router.register(r'projekty', ProjektViewSet)
router.register(r'mwds', MWDViewSet)

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^api/', include(router.urls)),
)