from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView
from projekty import views
from SSE import sse

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^sse/$',  sse.iterator),
    url(r'^api/reports/(?P<file_name>.+)/$',  views.get_report_file),
    url(r'^api/reports/$',  views.get_reports),
    url(r'^api/projekty/(?P<project_id>.+)/generate/$',  views.generate_report),
    url(r'^api/projekty/(?P<project_id>.+)/$',  views.project_details),
    url(r'^api/projekty/$',  views.projects_list),
    url(r'^api/mwds/$',  views.mwd_list),
)