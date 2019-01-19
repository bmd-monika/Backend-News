from django.conf.urls import url
from src.topics import views

urlpatterns = [
    url(r'^$', view=views.TopicsView.as_view()),
    url(r'^/(?P<id>[\w\-]+)$', view=views.TopicsView.as_view()),
]