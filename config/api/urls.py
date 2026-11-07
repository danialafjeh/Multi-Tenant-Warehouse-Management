from django.urls import path
from api.views import ProductInventoryAPIView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)



urlpatterns = [
    path("products/<str:sku>/inventory/", ProductInventoryAPIView.as_view(), name="product_inventory_api"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
