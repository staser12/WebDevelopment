from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Assign3_ipatkov.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^meta/$','Blog.views.display_meta'),
    #url(r'^datetime/$','Blog.views.current_datetime'),
    url(r'^myblog/$','Blog.views.show_home'),#valmis
    url(r'^editblog/(?P<id>\w+)/$','Blog.views.edit_blog'),
    url(r'^myblog/(?P<id>\w+)/$','Blog.views.show_blog'),
    url(r'^addblog/$','Blog.views.add_blog'),#valmis
    url(r'^deleteblog/(?P<id>\w+)/$','Blog.views.delete_blog'),
    url(r'^createuser/','Blog.views.create_user'),

    url(r'^admin/', include(admin.site.urls)),
)
