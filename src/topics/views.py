from django.shortcuts import render

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from  src.topics.models import Topics
from src.topics.serializers import topicsSerializer
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q

from src.helper.helpers import response, setDefaultValue

@method_decorator(csrf_exempt, name='dispatch')
class TopicsView(APIView):
    def get(self, request, id='', format=None):
        meta = None
        if request.method == 'GET':
            try:
                if id == '':
                    page = int(request.GET.get('page', 1))
                    limit = int(request.GET.get('limit', 10))

                    listTopics = Topics.objects.filter(is_delete=False).order_by('id')

                    paginator = Paginator(listTopics, limit)

                    res = topicsSerializer(paginator.page(page), many=True)

                    meta = {
                        "page": page,
                        "limit": limit,
                        "totalPages": paginator.num_pages,
                        "totalRecords": paginator.count
                    }

                    cleanData = list(map(lambda item: restructureJson(item), res.data))

                else:
                    try:
                        detailTopics = Topics.objects.get(pk=id,is_delete=False)
                    except Topics.DoesNotExist:
                        detailTopics = None
                        return response(404, message="Topics doesn't exists")

                    serializerTopics= topicsSerializer(detailTopics)
                    cleanData = restructureJson(serializerTopics.data)

                if cleanData:
                    message = "Get Topics" if id == '' else "Get Topics Detail"
                    status = True

                    return response(200, cleanData, message, status, meta)

                else:
                    return response(200, data=[], message='data not found', status=True)

            except Exception as e:
                return response(400, message=str(e))

    @method_decorator(transaction.atomic, name='dispatch')
    def post(self, request, *args, **kwargs):
        """
        Create topics
        """

        if request.method == 'POST':
            data = JSONParser().parse(request)
            topics = setDefaultValue('topics', data, '')
            if topics == '':
                return response(400, message="Field topics is required")

            cleanData = structureJson(data)

            serializer = topicsSerializer(data=cleanData)

            try:
                # Start Transaction
                sid = transaction.savepoint()

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                    message = "Success to Create Topics"
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
                topics = Topics.objects.get(pk=id)
            except Exception as e:
                return response(400, message=str(e))

            get_topics = topicsSerializer(topics).data
            # dp = department.approval_number
            cleanData = structureJson(data)
            serializer = topicsSerializer(topics, data=cleanData)
            # start transaction
            sid = transaction.savepoint()

            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                    message = "Success to update Topics"
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
        Delete Topics
        """
        try:
            getTopics = Topics.objects.get(pk=id, is_delete=False)
        except:
            return response(404, message="Topics not found")

        if request.method == 'DELETE':
            try:
                topics = Topics.objects.filter(pk=id).update(is_delete=True)

                if topics:
                    message = "Success to delete topics"
                    status = True

                    return response(201, message=message, status=status)

            except Exception as e:
                return response(400, message="Bad Request")

def structureJson(item):
    data = {
        "topics": item['topics'],
    }

    return data

def restructureJson(item):
    data = {
        "id": item['id'],
        "topics": item['topics'],
    }
    return data
