from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from projekty.models import Projekt, ProjektSerializer, MWD, MWDSerializer
from messaging.tasks import gen_report
from messaging.queue import ReportConsumerQueue
import logging, os

logger = logging.getLogger(__name__+'views')
subscriber = ReportConsumerQueue('reportReturnQueue', 'amqp://iypkanhf:f7W5aI8SOzDje6BM-e-JSPcR4k7V7VFh@turtle.rmq.cloudamqp.com:5672/iypkanhf').consume()

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

@api_view(['GET', 'POST'])
def project_details(request, project_id):
    if request.method == 'GET':
            projekts = Projekt.objects.filter(id=project_id)
            projektsSerializer = ProjektSerializer(projekts, many=True)
            return Response(projektsSerializer.data[0])
        
    elif request.method == 'POST':
            projekt = Projekt.objects.filter(id=project_id)[0]
            mwds=request.DATA['mwds']
            projekt.name = request.DATA['name']
            projekt.jira_URL = request.DATA['jira_URL']
            projekt.start_date = request.DATA['start_date']
            projekt.save()
            for mwd in mwds:
                projekt.addMwd(mwd)
            projektsSerializer = ProjektSerializer(projekt)
            return Response(projektsSerializer.data)
            
@api_view(['GET', 'POST'])
def projects_list(request):
    if request.method == 'GET':
        projekts = Projekt.objects.all()
        projektsSerializer = ProjektSerializer(projekts, many=True)
        return Response(projektsSerializer.data)

    elif request.method == 'POST':
        mwds=request.DATA['MWDs']
        del request.DATA['MWDs']
        projekt = Projekt(
                          name=request.DATA['name'], 
                          jira_URL=request.DATA['jira_URL'],
                          start_date=request.DATA['start_date'],
                          )       
        projekt.save()
        if mwds:
            for mwd in mwds:
                projekt.addMwd(mwd)
                
            serializer = ProjektSerializer(projekt)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def mwd_list(request):
    if request.method == 'GET':
        mwds = MWD.objects.all()
        mwdsSerializer = MWDSerializer(mwds, many=True)
        return Response(mwdsSerializer.data)

    elif request.method == 'POST':
        serializer = MWDSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def generate_report(request, project_id):
    if request.method == 'POST':
        logger.error('---------------------Generuje raport dla projektu o id: '+str(project_id)+' ---------------') 
        gen_report.delay(project_id)
        
@api_view(['GET', 'POST'])
def get_reports(request):
    if request.method == 'GET':
        path = '/var/lib/openshift/54646c675973ca5701000018/app-root/runtime/repo/reports/'
        files_list = os.listdir(path)
        return Response({'reports': files_list}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def get_report_file(request, file_name):
    if request.method == 'GET':
        path = '/var/lib/openshift/54646c675973ca5701000018/app-root/runtime/repo/reports/'
        logger.error('Pobieranie pliku '+(path+file_name)) 
        return_file=open(path+file_name, 'rb')
        response = HttpResponse(return_file, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        return response