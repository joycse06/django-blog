from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
            url(r'', TemplateView.as_view(template_name='static_pages/index.html'))
            )