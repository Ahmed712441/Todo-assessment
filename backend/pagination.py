from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class BasePaginator(PageNumberPagination):
    page_size = 9
    max_page_size = 9

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'results': data
        })