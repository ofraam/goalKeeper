from django.conf.urls import url

from gk import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]

#urlpatterns += staticfiles_urlpatterns()