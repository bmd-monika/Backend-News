from django.conf.urls import url
from src.news import views

urlpatterns = [
    url(r'^$', view=views.NewsView.as_view()),
    url(r'^/(?P<id>[\w\-]+)$', view=views.NewsView.as_view()),
]