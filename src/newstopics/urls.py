from django.conf.urls import url
from src.newstopics import views

urlpatterns = [
    url(r'^$', view=views.NewsTopicsView.as_view()),
    url(r'^/(?P<id>[\w\-]+)$', view=views.NewsTopicsView.as_view()),
]