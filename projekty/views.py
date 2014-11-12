from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from projekty.models import Projekt, ProjektSerializer, MWD, MWDSerializer


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
            projekt.name = request.DATA['name']
            projekt.jira_URL = request.DATA['jira_URL']
            projekt.start_date = request.DATA['start_date']
            projekt.save()
            mwds=request.DATA['mwds']
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