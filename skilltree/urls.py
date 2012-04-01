from django.conf.urls import patterns, include, url
from skilltree.views import SkillTreeView

urlpatterns = patterns('',
    url(r'^$', SkillTreeView.as_view()),
)
