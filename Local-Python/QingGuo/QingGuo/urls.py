"""QingGuo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

from QGAPP import views
from QingGuo.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^$', views.Home),
    url(r'^about/', views.About),
    url(r'^study/', views.Study),
    url(r'^studyVideo/', views.StudyVideo),
    url(r'^getStudyVideo/', views.GetStudyVideo),
    url(r'^gallery/', views.Gallery),
    url(r'^home/', views.Home),
    url(r'^schedule/', views.Schedule),
    url(r'^SaveRecord/', views.SaveRecord),
    url(r'^GetSchedule/', views.GetSchedule),
    url(r'^TextCat/', views.TextCat),
]
