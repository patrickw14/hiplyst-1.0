# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'Player.views.home', name='home'),
    # url(r'^Player/', include('Player.foo.urls')),

    (r'^$', 'player.views.full'),
    (r'^register/$', 'player.views.register'),
    (r'^login/$', 'player.views.login'),
    (r'^logout/$', 'player.views.logout'),

    (r'^ajax/report_bad_token/$', 'player.views.bad_token'),
    (r'^ajax/playlist/', include('playlists.urls')),

    (r'^add_token', 'player.views.add_token'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^new/(.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT + "/new", 'show_indexes': True}),
        (r'^css/(.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT + "/css", 'show_indexes': True}),
        (r'^images/(.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT + "/images", 'show_indexes': True}),
        (r'^js/(.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT + "/js", 'show_indexes': True}),
        (r'^swf/(.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT + "/swf", 'show_indexes': True}),
    )
