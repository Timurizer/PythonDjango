from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'note_manager'
urlpatterns = [
    url(r'^(?P<sorttype>\w+)$', views.IndexViewVarious.as_view(), name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^favourite_list/$', views.favourite_list, name='favourite_list'),
    url(r'^edit/$', views.edit_view, name='edit'),
    url(r'^add/$', views.add_note, name='add_note'),
    url(r'^contact/$', views.contact_us_view, name='contact'),
    url(r'^login/$', auth_views.login, {'template_name': 'note_manager/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/note_manager'}, name='logout'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail_view, name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit$', views.edit_view, name='edit'),
    url(r'^(?P<pk>[0-9]+)/add_favourite$', views.favourite, name='add_favourite'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^login/ajax/find_username/$', views.find_username, name='find_username'),

]
