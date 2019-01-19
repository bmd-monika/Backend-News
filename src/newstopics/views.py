from django.shortcuts import render

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from src.news.models import News
from src.news.serializers import newsSerializer
from src.topics.models import Topics
from src.topics.serializers import topicsSerializer
from  src.newstopics.models import NewsTopics
from src.newstopics.serializers import newsTopicsSerializer
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q

from src.helper.helpers import response, setDefaultValue

@method_decorator(csrf_exempt, name='dispatch')
class NewsTopicsView(APIView):
    def get(self, request, id='', format=None):
        meta = None
        if request.method == 'GET':
            try:
                if id == '':
                    page = int(request.GET.get('page', 1))
                    limit = int(request.GET.get('limit', 10))
                    status = request.GET.get('status', '')
                    topics = request.GET.get('topics', '')

                    if status != '' and status != 'DRAFT' and status != 'DELETED' and status != 'PUBLISH':
                        return response(400, message="Status Not Found")

                    if status != '' or topics != '':
                        keywords = Q()
                        if status:
                            keywords |= Q(news__status=status)

                        if topics:
                            keywords &= Q(topics=topics)

                        keywords &= Q(is_delete=False)
                        listNews = NewsTopics.objects.filter(keywords).order_by('id')
                    else:
                        listNews = NewsTopics.objects.filter(is_delete=False).order_by('id')

                    paginator = Paginator(listNews, limit)

                    res = newsTopicsSerializer(paginator.page(page), many=True)

                    meta = {
                        "page": page,
                        "limit": limit,
                        "totalPages": paginator.num_pages,
                        "totalRecords": paginator.count
                    }

                    cleanData = list(map(lambda item: restructureJson(item), res.data))

                else:
                    try:
                        detailNews = NewsTopics.objects.get(pk=id,is_delete=False)
                    except NewsTopics.DoesNotExist:
                        detailNews = None
                        return response(404, message="News doesn't exists")

                    serializerNews= newsTopicsSerializer(detailNews)
                    cleanData = restructureJson(serializerNews.data)

                if cleanData:
                    message = "Get News" if id == '' else "Get News Detail"
                    status = True

                    return response(200, cleanData, message, status, meta)

                else:
                    return response(200, data=[], message='data not found', status=True)

            except Exception as e:
                return response(400, message=str(e))

    @method_decorator(transaction.atomic, name='dispatch')
    def post(self, request, *args, **kwargs):
        """
        Create news
        """

        if request.method == 'POST':
            data = JSONParser().parse(request)
            news = setDefaultValue('news', data, '')
            topics = setDefaultValue('topics', data, '')
            if news == '':
                return response(400, message="Field news is required")
            if topics == '':
                return response(400, message="Field topics is required")

            cleanData = structureJson(data)

            serializer = newsTopicsSerializer(data=cleanData)

            try:
                # Start Transaction
                sid = transaction.savepoint()

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                    message = "Success to Create News"
                    status = True

                    res = restructureJson(serializer.data)


                    transaction.savepoint_commit(sid)

                    return response(201, res, message, status)

                transaction.savepoint_rollback(sid)
            except Exception as e:
                if serializer.errors:
                    return response(400, message=serializer.errors)

                return response(400, message=str(e))

    @method_decorator(transaction.atomic, name='dispatch')
    def put(self, request, id, *args, **kwargs):

        if request.method == 'PUT':
            data = JSONParser().parse(request)

            try:
                news = NewsTopics.objects.get(pk=id)
            except Exception as e:
                return response(400, message=str(e))

            get_news = newsTopicsSerializer(news).data
            # dp = department.approval_number
            cleanData = structureJson(data)
            serializer = newsTopicsSerializer(news, data=cleanData)
            # start transaction
            sid = transaction.savepoint()

            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                    message = "Success to Update news"
                    status = True

                    transaction.savepoint_commit(sid)

                    res = restructureJson(serializer.data)

                    return response(201, res, message, status)


            except Exception as e:
                transaction.savepoint_rollback(sid)

                return response(400, message=str(e))

    @csrf_exempt
    def delete(self, request, id='', *args, **kwargs):
        """
        Delete News
        """
        try:
            getNews = NewsTopics.objects.get(pk=id, is_delete=False)
        except:
            return response(404, message="News not found")

        if request.method == 'DELETE':
            try:
                news = NewsTopics.objects.filter(pk=id).update(is_delete=True)

                if news:
                    message = "Success to delete news"
                    status = True

                    return response(201, message=message, status=status)

            except Exception as e:
                return response(400, message="Bad Request")

def structureJson(item):
    data = {
        "news": item['news'],
        "topics": item['topics'],
    }

    return data

def restructureJson(item):
    test = 1
    news = newsSerializer(News.objects.get(pk=item['news'])).data
    topics = topicsSerializer(Topics.objects.get(pk=item['topics'])).data
    data = {
        "id": item['id'],
        "news": news,
        "topics": topics,
    }
    return data
