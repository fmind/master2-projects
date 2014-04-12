from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # weditor
    url(r'^$', 'weditor.views.index', name='index'),
    url(r'^accueil$', 'weditor.views.home', name='home'),
    url(r'^recherche$', 'weditor.views.search', name='search'),
    url(r'^cree$', 'weditor.views.create', name='create'),
    url(r'^integre/(\w+)$', 'weditor.views.link', name='link'),
    url(r'^modifie/(\d+)$', 'weditor.views.edit', name='edit'),
    url(r'^supprime/(\d+)$', 'weditor.views.delete', name='delete'),
    url(r'^recharge/(\d+)/(\d+)$', 'weditor.views.review', name='review'),
    url(r'^profil$', 'weditor.views.profile', name='profile'),
    url(r'^configure$', 'weditor.views.settings', name='settings'),
    url(r'^inscrit$', 'weditor.views.subscribe', name='subscribe'),
    url(r'^connecte$', 'weditor.views.login', name='login'),
    url(r'^deconnecte$', 'weditor.views.logout', name='logout'),

    # other apps
    url(r'^captcha/', include('captcha.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^wxcvbn/', include(admin.site.urls)),

    # Static and media files
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
