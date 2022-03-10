from rest_framework import pagination

class LargePagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class MaxPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    # max_page_size = 100