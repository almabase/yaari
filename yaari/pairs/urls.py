from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ActivePairsView.as_view()),
    url(r'^history/?$', views.HistoryView.as_view()),
]