from django.conf.urls import url

from gk import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^goal/$', views.goal, name='goal'),
    url(r'^action/$', views.action, name='goal'),
    url(r'^contacts/$', views.contacts, name='goal'),
    url(r'^profile/$', views.profile, name='goal'),
]

#urlpatterns += staticfiles_urlpatterns()