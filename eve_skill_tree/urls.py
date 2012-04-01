from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eve_skill_tree.views.home', name='home'),
    # url(r'^eve_skill_tree/', include('eve_skill_tree.foo.urls')),

    url(r'^', include("skilltree.urls")),

    url(r'^admin/', include(admin.site.urls)),
)
