from django.conf.urls import url

from member import views

app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login_fbv, name='login'),
    url(r'^login/facebook/$', views.login_facebook, name='login_facebook'),
    url(r'^logout/$', views.logout_fbv, name='logout'),
]
