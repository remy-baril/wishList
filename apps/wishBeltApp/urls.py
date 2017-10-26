from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^add$', views.addPage),
    url(r'^addItem$', views.addItem),
    url(r'^wish_items/(?P<item_id>\d+)$', views.itemPage),
    url(r'^delete/(?P<item_id>\d+)$', views.deleteItem),
]