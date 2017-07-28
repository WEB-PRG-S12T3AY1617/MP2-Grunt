from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    url(r'^(?P<username_id>[0-9]+)/$', views.profile, name='profile'),

    # add an item
    url(r'^item/add/$', views.ItemCreate.as_view(success_url="/home/"), name='item-add'),

    # update an item
    url(r'item/(?P<pk>[0-9]+)/$', views.ItemUpdate.as_view(), name='item-update'),

]








