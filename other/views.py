from rest_framework import pagination, viewsets
from rest_framework.parsers import FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from other.models import Project
from other.serializer import ProjectSerializer


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        limit = self.request.GET.get('limit', self.page_size)
        next_page = None
        previous_page = None
        if self.page.has_next():
            next_page = self.page.next_page_number()
        if self.page.has_previous():
            previous_page = self.page.previous_page_number()
        return Response({
            'next': self.get_next_link(),
            'next_page': next_page,
            'previous': self.get_previous_link(),
            'previous_page': previous_page,
            'count': self.page.paginator.count,
            'limit': int(limit),
            'results': data,
        })


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ImporterView(APIView):
    parser_classes = (FormParser,)

    def post(self, request):
        print(request.POST)
        print(request.FILES)
        print(request.data)
        return Response(status=200)



