from .serializers import SaleSerializer, CatalogSerializer
from django.core.paginator import Paginator


class SalePaginator(Paginator):

    """Пагинатор распродажи товаров"""

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        super().__init__(
            object_list,
            per_page,
            orphans=orphans,
            allow_empty_first_page=allow_empty_first_page,
        )

    def get_paginated_data(self, page_number):
        page = self.get_page(page_number)
        items = SaleSerializer(page, many=True).data
        return {
            "items": items,
            "currentPage": page_number,
            "lastPage": self.num_pages,
        }


class CatalogPaginator(Paginator):

    """Пагинатор каталога товаров"""

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        super().__init__(
            object_list,
            per_page,
            orphans=orphans,
            allow_empty_first_page=allow_empty_first_page,
        )

    def get_paginated_data(self, page_number):
        page = self.get_page(page_number)
        items = CatalogSerializer(page, many=True).data
        return {
            "items": items,
            "currentPage": page_number,
            "lastPage": self.num_pages,
        }
